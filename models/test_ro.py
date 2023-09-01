"""
Copyright (C) 2017-2021 Andrei Damian, andrei.damian@me.com,  All rights reserved.

This software and its associated documentation are the exclusive property of the creator.
Unauthorized use, copying, or distribution of this software, or any portion thereof,
is strictly prohibited.

Dissemination of this information or reproduction of this material is strictly forbidden unless prior
written permission from the author




"""
import torch as th

from time import time

from basic_inference_server import Logger
from models.llm_util import TransformerHelper

  
  
  
if __name__ == '__main__':
  TEST_LLAMA  = True    
  TEST_FULL   = False  
  TEST_STEP   = False
  
  PROMPTS = [
    'Capitala Frantei este:',
    
    'Cat face 2 + 2?',
    
    'Cine esti?',
    
    'Cu ce ma poti ajuta?',
    
    """Asteroidea este denumirea unei clase taxonomice din care fac parte stelele de mare.
    Asteroideele sunt animale marine care fac parte din ordinul Echinodermata.
    Stelele de mare cuprind un număr mare de specii care trăiesc în mediul marin, în apropierea coastelor, preferă locurile stâncoase, dar pot fi întâlnite și la adâncimi de 9.000 m, pe nisip sau pe substraturi vegetale.
    Din studiul fosilelor s-a constatat că stelele de mare există de peste 300 milioane de ani.
    Un reprezentant mai cunoscut al grupei este specia Asterias rubens
    In baza acestui text raspundeti la urmatoarea intrebare: Ce sunt stelele de mare?"""
  ]
  
  l = Logger('ROLLM', base_folder='.', app_folder='_cache')
  
  if TEST_LLAMA:
    models = [
      'ro-llama-2-13', 
      'ro-llama-2-7'
    ]
    precisions = ['float16', 'float32']
    for precision in precisions:
      for model_name in models:
        eng = TransformerHelper(
          name=model_name, 
          log=l,           
          cache_dir='/Lummetry.AI Dropbox/DATA/__LLMs',
          device_map="balanced", 
          torch_dtype=th.float16 if precision == 'float16' else th.float32
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
    
  
  if TEST_FULL or TEST_STEP:
    MODEL_FOLDER = '/Lummetry.AI Dropbox/DATA/__LLMs/models--readerbench--RoGPT2-medium/snapshots/7e75ef2461b5aba00b8d3c92e56da20c12b8030a'
    eng1 = TransformerHelper(name='r1', log=l, cache_dir='/Lummetry.AI Dropbox/DATA/__LLMs')
  
  if TEST_STEP:
    with th.no_grad():
      WARMS     = [] #[0,1]
      QUESTION  = 2
      m1 = eng1.model
      #warmup
      inputs = [eng1.tokenize(x) for x in PROMPTS]
      for _ in range(2):
        for i in WARMS:
          l.start_timer('fw')
          _ = m1(inputs[i])
          l.stop_timer('fw')
  
      l.start_timer('fw')
      res1 = m1(inputs[QUESTION])
      l.stop_timer('fw')
      tokens = res1.logits.argmax(-1)[0]
      txt1 = eng1.decode(tokens, input_text=None)
      print('inputs: ',inputs[QUESTION])
      print('logits: ',res1.logits.max(-1))
      print('text1: ', txt1)
      
      pad_token_id = eng1.tokenizer.eos_token_id
  
      for _ in range(2):
        for i in WARMS:
          l.start_timer('gen')
          _ = m1.generate(inputs[i], max_length=50, pad_token_id=pad_token_id,)
          l.stop_timer('gen')
  
      l.P("Running generate on {}".format(inputs[QUESTION]))
      l.start_timer('gen')
      res2 = m1.generate(inputs[QUESTION], max_length=50, pad_token_id=pad_token_id)
      l.stop_timer('gen')
      txt2 = eng1.decode(res2, input_text=None)
      print(txt2)
      
      l.P("Running engine step generate on {}".format(PROMPTS[QUESTION]))
      txt3 = eng1.step_greedy_generate(PROMPTS[QUESTION])
      print()
      print(txt3)
      
      txt4 = eng1.generate(PROMPTS[QUESTION])
      print()
      print(txt3)
      
      l.show_timers()
    
  
  if TEST_FULL:
    eng2 = TransformerHelper(name='r2', log=l)
    engines = [eng1, eng2]  
    mem = [round(x.model.get_memory_footprint() / (1024**3),2) for x in engines]
    l.P(f"Model footprints GB: {mem}")
    
    for prompt in PROMPTS:
      for eng in engines:
        for setting, color in zip(['normal', 'c1', 'c3', 's3'], [None, 'b', 'y', 'm']):
          text = eng.generate(prompt, setting=setting)
          l.P("Result for {} on '{}...', setting: {}:".format(
            eng.name, prompt[:20], setting), 
            color='g'
          )
          l.P("Text:\n{}".format(text), color=color)
      