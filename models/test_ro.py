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

from time import time


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


from basic_inference_server import Logger
from models.llm_util import TransformerHelper

  
  
  
if __name__ == '__main__':
  
  PROMPTS = [
    'Capitala Frantei este:',
    
    'Cat face 2 + 2?',
    
    'Cine esti?',
    
    'Cu ce ma poti ajuta?',
    
    """Asteroidea este denumirea unei clase taxonomice din care fac parte stelele de mare.
    Asteroideele sunt animale marine.
    In baza acestui text raspundeti la urmatoarea intrebare: Ce sunt stelele de mare?"""
  ]
  
  l = Logger('ROLLM', base_folder='.', app_folder='_cache')
  
  if TEST_LLAMA:
    models = [
      # "/Lummetry.AI Dropbox/DATA/__LLMs/_snapshot_llama2_7_ro_v1"
      'llama-2-70'
      #'ro-llama-2-13', 
      #'ro-llama-2-7'
    ]
    precisions = ['float16'] #, 'float32']
    for precision in precisions:
      for model_name in models:
        eng = TransformerHelper(
          name=model_name, 
          log=l,           
          cache_dir='/Lummetry.AI Dropbox/DATA/__LLMs',
          device_map="balanced", 
          torch_dtype=th.float16 if precision == 'float16' else th.float32,
          ###
          use_auth_token=os.environ['HF_TOKEN'],
          ###
        )
        setting = 'normal'
        dtype = str(next(eng.model.parameters()).dtype).split('.')[-1]
        l.P("Generating with {}:{} => {}".format(model_name, dtype, eng.placement_summary()), color='y')
        for prompt in PROMPTS:
          l.start_timer(model_name + '-' + dtype)
          text = eng.generate(prompt, setting=setting)
          l.stop_timer(model_name + '-' + dtype)
          l.P("Result for {} on '{}...', setting: {}:".format(
            eng.name, prompt[:50], setting), 
          )
          l.P("Text:\n{}".format(text), color='g')
        del eng.model
        del eng
    
  eng = TransformerHelper(
    name=model_name, 
    log=l,           
    cache_dir='/Lummetry.AI Dropbox/DATA/__LLMs',
    device_map="balanced", 
    torch_dtype=th.float16
  )
  dtype = str(next(eng.model.parameters()).dtype).split('.')[-1]
  l.P("Generating with {}:{} => {}".format(model_name, dtype, eng.placement_summary()), color='y')

  setting = 'normal'
  text1 = eng.generate(prompt1, setting=setting)
  l.P("`{}` results:\n{}".format(prompt1, text1), color='g')
  text2 = eng.generate(prompt2, setting=setting)
  l.P("`{}` results:\n{}".format(prompt2, text2), color='g')

