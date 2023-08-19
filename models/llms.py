"""
Copyright (C) 2017-2021 Andrei Damian, andrei.damian@me.com,  All rights reserved.

This software and its associated documentation are the exclusive property of the creator.
Unauthorized use, copying, or distribution of this software, or any portion thereof,
is strictly prohibited.

Dissemination of this information or reproduction of this material is strictly forbidden unless prior
written permission from the author

"""
import torch as th
import os


PATH = "./_cache/_models/llms"
os.makedirs(PATH, exist_ok=True)
os.environ["TRANSFORMERS_CACHE"] = PATH

from transformers import (
  GPT2LMHeadModel,
  GPTNeoForCausalLM, 
  GPTJForCausalLM,
  GPT2Tokenizer,
  
  T5ForConditionalGeneration,
  T5Tokenizer,
  
  AutoTokenizer, 
  AutoModelForCausalLM
)

from libraries import BaseObject

_CONFIG = {
  "ro-base" : {
    "name"        : "/WORK/812_LLModels/RoGPT2-base",
    "model"       : GPT2LMHeadModel,
    "tokenizer"   : GPT2Tokenizer,
  },

  "ro-medium" : {
    "name"        : "/WORK/812_LLModels/RoGPT2-medium",
    "model"       : GPT2LMHeadModel,
    "tokenizer"   : GPT2Tokenizer,
  },

  "ro-large" : {
    "name"        : "/WORK/812_LLModels/RoGPT2-large",
    "model"       : GPT2LMHeadModel,
    "tokenizer"   : GPT2Tokenizer,
  },

  
  "basic" : {
    "name"        : "gpt2",
    "model"       : GPT2LMHeadModel,   
    "tokenizer"   : GPT2Tokenizer,
  },
  "basic-med" : {
    "name"        : "gpt2-medium",
    "model"       : GPT2LMHeadModel,   
    "tokenizer"   : GPT2Tokenizer,
  },
  "basic-large" : {
    "name"        : "gpt2-large",
    "model"       : GPT2LMHeadModel,   
    "tokenizer"   : GPT2Tokenizer,
  },
  "basic-xl" : {
    "name"        : "gpt2-xl",
    "model"       : GPT2LMHeadModel,   
    "tokenizer"   : GPT2Tokenizer,
  },  
  
  "neo-s" : {
    "name"        : "EleutherAI/gpt-neo-1.3B",
    "model"       : GPTNeoForCausalLM,
    "tokenizer"   : GPT2Tokenizer,
  },
  
  "neo-l" : {
    "name"        : "EleutherAI/gpt-neo-2.7B",
    "model"       : GPTNeoForCausalLM,
    "tokenizer"   : GPT2Tokenizer,
  },

  "t5-s" : {
    "name"        : "t5-small",
    "model"       : T5ForConditionalGeneration,
    "tokenizer"   : T5Tokenizer,
    "input"       : "complete the sentence: {}",
    "bad_words"   : False,
    "override"  : dict(
        attention_mask=None,
        max_length=None, 
        num_return_sequences=None,
        pad_token_id=None,
        top_k=None, 
        top_p=None,
        do_sample=None, 
        temperature=None, 
        num_beams=None, 
        bad_words_ids=None,
        early_stopping=None,
        no_repeat_ngram_size=None,
        output_scores=None,
        return_dict_in_generate=None,
    )
  },


  "t5-b" : {
    "name"        : "t5-base",
    "model"       : T5ForConditionalGeneration,
    "tokenizer"   : T5Tokenizer,
    "input"       : "translate English to German: {}",
    "bad_words"   : False,
    "override"  : dict(
        attention_mask=None,
        max_length=None, 
        num_return_sequences=None,
        pad_token_id=None,
        top_k=None, 
        top_p=None,
        do_sample=None, 
        temperature=None, 
        num_beams=None, 
        bad_words_ids=None,
        early_stopping=None,
        no_repeat_ngram_size=None,
        output_scores=None,
        return_dict_in_generate=None,
    )
  },
  


  # "gptj" : {
  #   "name"        : "EleutherAI/gpt-j-6B",
  #   "model"       : GPTJForCausalLM,
  #   "tokenizer"   : GPT2Tokenizer,
  # },
  
}

BAD_WORDS = ['a', 'the', 'of', 'is', 'de', 'la', 'its', 'an']

AVAIL_MODELS = list(_CONFIG.keys())

class TransformerNet(BaseObject):
  def __init__(self, model_name, **kwargs):
    assert model_name in _CONFIG
    self.tokenizer = None
    self.model = None
    self.bad_words_ids = None
    self._model_name = model_name
    self._config = _CONFIG[model_name]
    super(TransformerNet, self).__init__(**kwargs)
    return
  
  def startup(self):
    self.P("Initializing '{}'".format(self._model_name))
    return


  def load_models(self):
    model_name = self._config['name']
    self.P("Loading '{}'...".format(model_name))
    self.tokenizer = self._config['tokenizer'].from_pretrained(model_name)
    self.bad_words_ids = None
    if self._config.get('bad_words', True):
      self.bad_words_ids = self.tokenizer(BAD_WORDS, add_prefix_space=True, add_special_tokens=False).input_ids
    self.model = self._config['model'].from_pretrained(model_name)
    self.P("Done loading models.")
    return


  def generate_next_word(self, 
                         text, 
                         n_samples=1, 
                         include_sentence=False,
                         top_k=None,
                         top_p=None, 
                         do_sample=None,
                         temperature=None,
                         num_beams=None,
                         early_stopping=None,
                         no_repeat_ngram_size=None,       
                         extra_tokens=10,
                         ):
    if text is None or len(text) < 10:
      raise ValueError("{} received invalid prompt {}".format(self.__class__.__name__, text))
    result = []
    n_words = 1
    formatter = self._config.get('input')
    if formatter is not None:
      text = formatter.format(text)
    input_ids = self.tokenizer.encode(text, return_tensors="pt")
    attention_mask = th.ones_like(input_ids)
    
    kwargs = dict(
        attention_mask=attention_mask,
        max_length=input_ids.shape[1] + n_words + extra_tokens, 
        num_return_sequences=n_samples,
        pad_token_id=self.model.config.eos_token_id,
        top_k=top_k, 
        top_p=top_p,
        do_sample=do_sample, 
        temperature=temperature, 
        num_beams=num_beams, 
        bad_words_ids=self.bad_words_ids,
        early_stopping=early_stopping,
        no_repeat_ngram_size=no_repeat_ngram_size,
        output_scores=True,
        return_dict_in_generate=True,
    )
    
    override = self._config.get('override')
    if override is not None:
      kwargs = {
        **kwargs,
        **override,
      }

    with th.inference_mode():
      res = self.model.generate(
        inputs=input_ids, 
        **kwargs,
      )
      
    if not isinstance(res, th.Tensor):
      outputs = res.sequences
      scores = res.scores[0]
    else:
      outputs = res
      scores = None
    _results = []
    for i in range(outputs.shape[0]):
      output = outputs[i]
      token = output[-1]
      score = scores[i][token] if scores is not None else -1
      out_text = self.tokenizer.decode(output, skip_special_tokens=True)
      lst_text = out_text.split()[-n_words:]
      res_text = ' '.join(lst_text)
      if res_text in _results:
        continue
      _results.append(res_text)
      if include_sentence:
        result.append((res_text, score, out_text))
      else:
        result.append((res_text, score))
    return result
  
  def shutdown(self):
    del self.model
    del self.tokenizer


if __name__ == '__main__':
  
  from libraries import Logger
  from collections import defaultdict
  import numpy as np
  MAX_ANS = 3
  prompts = [
    # "In what country is Normandy located?", 
    # "What is the symbol for Zinc?", 
    # "What kind of phenomena does science study?",
    # "What is considered a key part of interior design?",
    # "What color are tail lights?",
    "Paris este capitala",
    "Istambul este situat intre",
    "Suma patratelor catetelor este egala cu",
    "3 x 3 + 10 = ",
    "Radical din 9 este egal cu",
  ]
  results = defaultdict(lambda: [])

  l = Logger("TST", base_folder=".", app_folder="output")
  models = [
    # 'basic', 
    # 'ro-base',
    'ro-medium',
    # 'ro-large',
    # 'basic-medium', 
    # 'basic-large', 
    # 'basic-xl', 
    # 'neo-s',
    # 't5-b',
  ]
  for model in models:    
    eng = TransformerNet(model_name=model, log=l)
    eng.load_models()
    for prompt in prompts:
      base = eng.generate_next_word(text=prompt, n_samples=1, include_sentence=True)
      options = eng.generate_next_word(
        text=prompt, 
        n_samples=10, 
        include_sentence=True,
        top_k=50,
        top_p=0.98,
        do_sample=True,
        # early_stopping=True,
        # temperature=0.7,
        # num_beams=3,
        no_repeat_ngram_size=1,
      )
      
      results[prompt].append({
        'model' : model,
        'ans'   : base,
        'opt'   : options,
      })
    #endfor each prompt
    eng.shutdown()
    del eng
    
  for prompt in results:
    l.P("Question: {}".format(prompt))
    answers_by_model = results[prompt]
    for answer in answers_by_model:
      model = answer['model']
      l.P("  Model: '{}'".format(model))
      ans = answer['ans'][0][0]
      proba = answer['ans'][0][0]
      options = [x[0] for x in answer['opt'] if x[0] != ans]
      options = options[:2]
      options.append(ans)
      np.random.shuffle(options)
      l.P("    Answer: {}".format(ans))
      for i, opt in enumerate(options):
        l.P("    Option {}: {}".format(i, opt))
      l.P("  ")
