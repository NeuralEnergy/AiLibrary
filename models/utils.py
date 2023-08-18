# -*- coding: utf-8 -*-
"""
Copyright (C) 2017-2021 Andrei Damian, andrei.damian@me.com,  All rights reserved.

This software and its associated documentation are the exclusive property of the creator.
Unauthorized use, copying, or distribution of this software, or any portion thereof,
is strictly prohibited.

Dissemination of this information or reproduction of this material is strictly forbidden unless prior
written permission from the author

"""

import os
import torch as th
import numpy as np

PATH = "./_cache/_data/llms"
os.makedirs(PATH, exist_ok=True)
os.environ["TRANSFORMERS_CACHE"] = PATH


from transformers import AutoModelForCausalLM, AutoTokenizer

MODELS = {
  'r1' : 'readerbench/RoGPT2-medium',
  'r2' : 'readerbench/RoSummary-medium'
}

PARAMS = {
  "normal"  : dict(max_length=250),
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

def ro_sanitizer(text):
  text = text.replace("ţ", "ț").replace("ş", "ș").replace("Ţ", "Ț").replace("Ş", "Ș")
  text = text.replace('Summary:', 'In sumar:')
  return text


def _tokenize(input_text : str, tokenizer: AutoTokenizer):
  inputs = tokenizer.encode(input_text, return_tensors='pt')
  return inputs

def _generate(input_text : str, model : AutoModelForCausalLM, tokenizer : AutoTokenizer, **kwargs):
  inputs = _tokenize(input_text=input_text, tokenizer=tokenizer)
  
  outputs = model.generate(
    inputs, 
    pad_token_id=tokenizer.eos_token_id,
    **kwargs,
  )
  texts = []
  for output in outputs:
    output_text = tokenizer.decode(output, skip_special_tokens=True)
    text = output_text.replace(input_text, "").strip()  
    text = ro_sanitizer(text)
    texts.append(text)
  return texts

class TransformerHelper:
  def __init__(self, name, log):
    self.log = log
    assert name in MODELS
    self.name = MODELS[name]
    self.P("Initializing tokenizer {}".format(self.name), color='d')
    self.tokenizer = AutoTokenizer.from_pretrained(self.name)
    self.P("Loading model {} ...".format(self.name ), color='d')
    self.model = AutoModelForCausalLM.from_pretrained(self.name)
    self.P("Done loading model.", color='d')
    return
  
  def P(self, s, color=None):
    self.log.P(s, color=color)
    return
  
  def tokenize(self, input_text):
    return _tokenize(input_text=input_text, tokenizer=self.tokenizer)
  
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