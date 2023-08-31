# -*- coding: utf-8 -*-
"""
Copyright (C) 2017-2021 Andrei Damian, andrei.damian@me.com,  All rights reserved.

This software and its associated documentation are the exclusive property of the creator.
Unauthorized use, copying, or distribution of this software, or any portion thereof,
is strictly prohibited.

Dissemination of this information or reproduction of this material is strictly forbidden unless prior
written permission from the author


  greedy decoding:
    by calling greedy_search() if num_beams=1 and do_sample=False
  
  contrastive search:
    by calling contrastive_search() if penalty_alpha>0. and top_k>1
  
  multinomial sampling:
    by calling sample() if num_beams=1 and do_sample=True
  
  beam-search decoding:
    by calling beam_search() if num_beams>1 and do_sample=False
  
  beam-search multinomial sampling:
    by calling beam_sample() if num_beams>1 and do_sample=True
  
  diverse beam-search decoding:
    by calling group_beam_search(), if num_beams>1 and num_beam_groups>1
  
  constrained beam-search decoding:
    by calling constrained_beam_search(), if constraints!=None or force_words_ids!=None
  
  assisted decoding:
    by calling assisted_decoding(), if assistant_model is passed to .generate()
  

"""

import os
import re
import torch as th
import numpy as np

PATH = "./_cache/_models/llms"
os.makedirs(PATH, exist_ok=True)
os.environ["TRANSFORMERS_CACHE"] = PATH


from transformers import AutoModelForCausalLM, AutoTokenizer

STRIP_CHARS = ' -'

MODELS = {
  'r1'            : 'readerbench/RoGPT2-medium',
  'r2'            : 'readerbench/RoSummary-medium',
  'ro-llama-2-7'  : 'Photolens/llama-2-7b-langchain-chat',
  'ro-llama-2-13' : 'Photolens/llama-2-13b-langchain-chat',
}

PARAMS = {
  "normal"  : dict(max_new_tokens=100),
  "c3"      : dict(
                penalty_alpha=0.6, 
                top_k=4, 
                max_new_tokens=100, 
                do_sample=True, 
                num_return_sequences=3,
              ),
  'c1'      : dict(
                penalty_alpha=0.6, 
                top_k=4, 
                max_new_tokens=100
              ),
  's3'      : dict(
                temperature=0.8,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                no_repeat_ngram_size=2,
                num_return_sequences=3, 
                max_length=250,
              )
}


def split_into_sentences(paragraph):
  # The regular expression looks for sentence-ending characters followed by spaces, newlines, or another sentence-ending character.
  # The positive lookahead (?=...) ensures that the sentence-ending character is matched but not consumed, so it remains part of the resulting sentence.
  sentences = re.split(r'(?<=[.!?])(?=\s|\w)', paragraph)
  
  # Remove any trailing whitespace and return the list of sentences
  sentences = [sentence.strip() for sentence in sentences if sentence]
  for i in range(len(sentences)):
    sentences[i] = sentences[i][0].upper() + sentences[i][1:]
  return sentences

def ro_sanitizer(text):
  text = text.replace("ţ", "ț").replace("ş", "ș").replace("Ţ", "Ț").replace("Ş", "Ș")
  text = text.replace('Summary:', 'In sumar:')
  return text


def _tokenize(input_text : str, tokenizer: AutoTokenizer):
  th_inputs = tokenizer.encode(input_text, return_tensors='pt')
  return th_inputs


def _paragraph_cleaner(text, max_sentence=3):
  parts = split_into_sentences(text)
  output = " ".join(parts[:max_sentence])
  return output


def _decode(outputs, tokenizer : AutoTokenizer, input_text : str = None, max_sentence=3, **kwargs):
  texts = []
  for output in outputs:
    output_text = tokenizer.decode(output, skip_special_tokens=True)
    text = output_text
    if input_text is not None:
      text = text.replace(input_text, "").strip(STRIP_CHARS)  
    text = ro_sanitizer(text)
    text = _paragraph_cleaner(text, max_sentence=max_sentence)
    texts.append(text)
  return texts
  

def _generate(input_text : str, model : AutoModelForCausalLM, tokenizer : AutoTokenizer, **kwargs):
  th_inputs = _tokenize(input_text=input_text, tokenizer=tokenizer)
  
  dev = next(model.parameters()).device
  th_inputs = th_inputs.to(dev)
  
  outputs = model.generate(
    th_inputs, 
    pad_token_id=tokenizer.eos_token_id,
    **kwargs,
  )
  texts = _decode(outputs, tokenizer=tokenizer)
  return texts


class TransformerHelper:
  def __init__(self, name, log, **kwargs):
    self.log = log
    if name[0] != '/':      
      assert name in MODELS
      self.name = MODELS[name]
    else:
      self.name = name    
    self.kwargs = kwargs
    self.P("Initializing tokenizer {}".format(self.name), color='d')
    self.tokenizer = AutoTokenizer.from_pretrained(self.name, **kwargs)
    self.P("Loading model {} ...".format(self.name ), color='d')
    self.model = AutoModelForCausalLM.from_pretrained(self.name, **kwargs)
    self.P("Done loading model.", color='d')
    return
  
  
  def P(self, s, color=None):
    self.log.P(s, color=color)
    return
  
  def tokenize(self, input_text):
    return _tokenize(input_text=input_text, tokenizer=self.tokenizer)
  
  
  def decode(self, tokens, input_text=None):
    return _decode(outputs=tokens, tokenizer=self.tokenizer, input_text=input_text)
  
  def placement_summary(self):
    result = ""
    if hasattr(self.model, 'hf_device_map'):
      self.placement = self.model.hf_device_map
      device = None
      prev_layer = None
      for layer in self.placement:
        if device != self.placement[layer]:
          if device is not None:
            result = result + layer + ']:{} '.format(self.placement[prev_layer])
          device = self.placement[layer]
          result = result + '[{}->'.format(layer)
          prev_layer = layer
      result = result + layer + ']:{} '.format(self.placement[layer])
    return result
  
  
  def step_greedy_generate(self, input_text, callback=lambda x: print(x, end='', flush=True), max_len=50):  
    self.P("Generating step-by-step with {}:".format(self.name), color='d')
    th_input = _tokenize(input_text=input_text, tokenizer=self.tokenizer)
    th_curr_input = th_input
    n_generated = 0
    while True:
      res = self.model(th_curr_input)
      n_generated += 1
      th_next_token = res.logits.argmax(-1)[:, -1]
      curr_text = self.tokenizer.decode(th_next_token)
      callback(curr_text)
      th_curr_input = th.cat([th_curr_input, th_next_token.unsqueeze(0)], dim=-1)
      if th_next_token[0] == self.tokenizer.eos_token_id or n_generated >= max_len:
        break
    text = _decode(th_curr_input, tokenizer=self.tokenizer)
    return text
  
  
  def generate(self, input_text, setting='normal'):
    assert setting in PARAMS
    kwargs = PARAMS[setting]
    self.P("Generating with {}:{}".format(self.name, kwargs), color='d')
    texts = _generate(
      input_text=input_text,
      model=self.model,
      tokenizer=self.tokenizer,
      **kwargs,
    )
    result = None
    if len(texts) > 1:
      result = np.random.choice(texts)
    else:
      result = texts[0]
    return result