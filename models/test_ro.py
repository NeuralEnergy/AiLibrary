"""
Copyright (C) 2017-2021 Andrei Damian, andrei.damian@me.com,  All rights reserved.

This software and its associated documentation are the exclusive property of the creator.
Unauthorized use, copying, or distribution of this software, or any portion thereof,
is strictly prohibited.

Dissemination of this information or reproduction of this material is strictly forbidden unless prior
written permission from the author

r1:
  normal  :
  c3      : 
  c1      :
  s3      : +++

r2:
  normal  :
  c3      :
  c1      :
  s3      : + 

"""
import torch as th
import os

from time import time


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


from basic_inference_server import Logger
from models.llm_util import TransformerHelper

  
  
  
if __name__ == '__main__':
  l = Logger('ROLLM', base_folder='.', app_folder='_cache')
  
  models = [
    'r1',
    'r2',
  ] 
  prompts = [
    'Functionezi?',
    'Ce faci?',
    'Cum te cheama?',
  ]
  settings = [
    # 'normal',
    # 'c3',
    # 'c1',
    's3',
  ]
  
  for model_name in models:
    eng = TransformerHelper(
      name=model_name, 
      log=l,           
      cache_dir='/Lummetry.AI Dropbox/DATA/__LLMs',
      device_map="cpu", 
      debug=True,
      torch_dtype=th.float32,
      low_cpu_mem_usage=True,
    )
    for prompt in prompts:    
      for setting in settings:      
        text = eng.generate(prompt, setting=setting)
        l.P("<{}> '{}' results with setting `{}`:\n{}".format(model_name, prompt, setting, text), color='g')

