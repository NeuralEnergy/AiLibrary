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
import json
import os
import re
import torch as th
import numpy as np

PATH = "./_cache/_models/llms"
os.makedirs(PATH, exist_ok=True)
os.environ["TRANSFORMERS_CACHE"] = PATH

from time import time

from transformers import AutoModelForCausalLM, AutoTokenizer

STRIP_CHARS = ' -'

MODELS = {
  'r1'            : 'readerbench/RoGPT2-medium',
  'r2'            : 'readerbench/RoSummary-medium',
  'ro-llama-2-7'  : 'Photolens/llama-2-7b-langchain-chat',
  'ro-llama-2-13' : 'Photolens/llama-2-13b-langchain-chat',
  'llama-2-70'    : 'meta-llama/Llama-2-70b-chat-hf',
}

PARAMS = {
  "normal"  : dict(max_new_tokens=1000),
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





class TransformerHelper:
  def __init__(self, name, log, debug=False, **kwargs):
    self.log = log
    self.debug = debug
    if name[0] != '/':      
      assert name in MODELS
      self.name = MODELS[name]
      self.__display_name = name
    else:
      self.name = name  
      self.__display_name = name.split('/')[-1]  
    self.kwargs = kwargs
    t_start = time()
    self.P("Initializing tokenizer {}".format(self.name), color='d')
    self.tokenizer = AutoTokenizer.from_pretrained(self.name, **kwargs)
    self.P("Loading model {} ...".format(self.name ), color='d')
    self.model = AutoModelForCausalLM.from_pretrained(self.name, **kwargs)
    elapsed = time() - t_start
    self.P("Done loading model ({}) in {:.1f}s".format(next(self.model.parameters()).dtype, elapsed), color='d')
    self.P("  Placement: {}".format(self.placement_summary()), color='d')
    self.P("  Memory size: {:.1f} MB".format(self.model_size()), color='d')
    return
  
  
  def P(self, s, color=None):
    self.log.P("[{}] ".format(self.__display_name) + s, color=color)
    return
  
  def _split_into_sentences(self, paragraph):
    # The regular expression looks for sentence-ending characters followed by spaces, newlines, or another sentence-ending character.
    # The positive lookahead (?=...) ensures that the sentence-ending character is matched but not consumed, so it remains part of the resulting sentence.
    sentences = re.split(r'(?<=[.!?])(?=\s|\w)', paragraph)
    
    # Remove any trailing whitespace and return the list of sentences
    sentences = [sentence.strip() for sentence in sentences if sentence]
    for i in range(len(sentences)):
      sentences[i] = sentences[i][0].upper() + sentences[i][1:]
    return sentences

  def _ro_sanitizer(self, text):
    text = text.replace("ţ", "ț").replace("ş", "ș").replace("Ţ", "Ț").replace("Ş", "Ș")
    text = text.replace("”", '').replace("“", '').replace("„", '')
    text = text.replace('Summary:', 'In sumar:')
    return text  

  def _tokenize(self, input_text : str, tokenizer: AutoTokenizer):
    th_inputs = tokenizer.encode(input_text, return_tensors='pt')
    return th_inputs


  def _paragraph_cleaner(self, text, max_sentence=3):
    parts = self._split_into_sentences(text)
    output = " ".join(parts[:max_sentence])
    return output


  def _decode(self, outputs, tokenizer : AutoTokenizer, input_text : str = None, max_sentence=3, **kwargs):
    texts = []
    for output in outputs:
      output_text = tokenizer.decode(output, skip_special_tokens=True)
      text = output_text
      if input_text is not None:
        text = text.replace(input_text, "").strip(STRIP_CHARS)  
      text = self._ro_sanitizer(text)
      text = self._paragraph_cleaner(text, max_sentence=max_sentence)
      texts.append(text)
    return texts

  def _generate(
    self, 
    input_text : str, 
    model : AutoModelForCausalLM, 
    tokenizer : AutoTokenizer, 
    exclude_input : bool = True,
    **kwargs
  ):
    th_inputs = self._tokenize(input_text=input_text, tokenizer=tokenizer)
    
    dev = next(model.parameters()).device
    th_inputs = th_inputs.to(dev)
    
    outputs = model.generate(
      th_inputs, 
      pad_token_id=tokenizer.eos_token_id,
      **kwargs,
    )
    texts = self._decode(
      outputs, 
      tokenizer=tokenizer, 
      input_text=input_text if exclude_input else None, 
      **kwargs
    )
    return texts

  
  def tokenize(self, input_text):
    return self._tokenize(input_text=input_text, tokenizer=self.tokenizer)
  
  
  def decode(self, tokens, input_text=None):
    return self._decode(outputs=tokens, tokenizer=self.tokenizer, input_text=input_text)
  
  def model_size(self):
    n_params = self.model.num_parameters()
    dtype = str(next(self.model.parameters()).dtype)
    bits = int(''.join(filter(str.isdigit, dtype)))
    size = n_params * bits / 8 / (1024 ** 2)
    return size # in MB
  
  def placement_summary(self):
    result = ""
    if hasattr(self.model, 'hf_device_map'):
      self.placement = self.model.hf_device_map
      device = None
      prev_layer = None
      n = 0
      if len(self.placement) == 1:
        _layer = list(self.placement.keys())[0]
        result = str(self.placement[_layer])
      else:
        for layer in self.placement:
          if device != self.placement[layer]:
            if device is not None:
              result = result + prev_layer + ']({}):{} '.format(n, self.placement[prev_layer])
              n = 0
            device = self.placement[layer]
            result = result + '[{}->'.format(layer)
            prev_layer = layer          
          n += 1
        result = result + layer + ']({}):{} '.format(n, self.placement[layer])
    return result
  
  
  def step_greedy_generate(self, input_text, callback=lambda x: print(x, end='', flush=True), max_len=50):  
    self.P("Generating step-by-step with {}:".format(self.name), color='d')
    th_input = self._tokenize(input_text=input_text, tokenizer=self.tokenizer)
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
    text = self._decode(th_curr_input, tokenizer=self.tokenizer)
    return text
  
  
  def generate(self, input_text, setting='normal'):
    assert setting in PARAMS
    kwargs = PARAMS[setting]
    self.P("Generating with {} ({}):{}".format(self.name, setting, kwargs), color='d')
    t_start = time()
    texts = self._generate(
      input_text=input_text,
      model=self.model,
      tokenizer=self.tokenizer,
      **kwargs,
    )
    n_outputs = len(texts)
    elapsed = time() - t_start
    self.P("  Done generating {} results in {:.1f}s".format(n_outputs, elapsed), color='d')
    if n_outputs > 1 and self.debug:
      self.P("  Results:\n{}".format(json.dumps(texts, indent=2)), color='d')
    result = None
    if n_outputs > 1:
      result = np.random.choice(texts)
    else:
      result = texts[0]
    return result