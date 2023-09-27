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
  l = Logger('ROLLM', base_folder='.', app_folder='_cache')
  
  model_name = 'ro-llama-2-7'
  prompt1 = 'Capitala Frantei este :'
  prompt2 = "[INST] Capitala Frantei este : [/INST]"
    
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
  text2 = eng.generate(prompt2, setting=setting)
  l.P("`{}` results:\n{}".format(prompt2, text2), color='g')

  text1 = eng.generate(prompt1, setting=setting)
  l.P("`{}` results:\n{}".format(prompt1, text1), color='g')

