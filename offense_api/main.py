#
# Neural Energy Power Plant project 
#
# @Author: Neuroplastic Software SRL
# @Copyright: Neural Energy SRL
# @description: FastAPI wrapper for the ReaderBench Ro-Offense model
# @Date: 2022-10-01
# @Last Modified by:   Neuroplastic Software SRL
# 


import json
import torch as th
import numpy as np
import pkg_resources

from collections import deque
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from time import time
from uuid import uuid4

__VER__ = '0.1.1'

CACHE_DIR = './_models_cache'
MODEL_NAME = "readerbench/ro-offense"

MANDATORY_PACKAGES = ['transformers', 'tokenizers', 'fastapi','torch']

# Function to get packages
def get_packages(monitored_packages=None):
    packs = [x for x in pkg_resources.working_set]
    maxlen = max([len(x.key) for x in packs]) + 1
    if isinstance(monitored_packages, list) and len(monitored_packages) > 0:
        packs = [
            "{}{}".format(x.key + ' ' * (maxlen - len(x.key)), x.version) for x in packs
            if x.key in monitored_packages
        ]
    else:
        packs = [
            "{}{}".format(x.key + ' ' * (maxlen - len(x.key)), x.version) for x in packs
        ]
    packs = sorted(packs)
    return packs
  
  
class ModelHelper:
  def __init__(self, model_name=MODEL_NAME, cache_dir=CACHE_DIR):
    self.__model_name = model_name
    self.__cache_dir = cache_dir
    self.__tokenizer = None
    self.__model = None
    self.__app_device = None
    self.__packs = None
    self.__timings = deque(maxlen=1000)
    self.__packs_mandatory = None
    self.__init()
    return
  
  def P(self, s, **kwargs):
    print(s, flush=True)
    return
  
  def __init(self):
    self.P("Initializing model helper ...", flush=True)
    self.__packs = get_packages()
    self.P("Packages: \n{}".format("\n".join(self.__packs)), flush=True)
    self.__packs_mandatory = [x for x in self.__packs if x.split()[0] in MANDATORY_PACKAGES]
    self._local_id = str(uuid4())[:8]
    return
  
  
  def build(self):
    self.P("Building model helper ...")
    self.__tokenizer = AutoTokenizer.from_pretrained(self.__model_name, cache_dir=self.__cache_dir)
    self.__model = AutoModelForSequenceClassification.from_pretrained(self.__model_name, cache_dir=self.__cache_dir)
    if th.cuda.is_available():
      self.__app_device = th.device('cuda:0')
    else:
      self.__app_device = th.device('cpu')
    self.__model = self.__model.to(self.__app_device)
    
    if th.cuda.is_available():
      self.P("GPU: {}".format(th.cuda.get_device_name(0)), flush=True) 
    else:
      self.P("GPU: Not available", flush=True)
    
    WARMUP_TEXT = "Esti destept!"
    results = self.run_predict(text=WARMUP_TEXT, timeit=False)
    self.P("Warmup on '{}': {}".format(WARMUP_TEXT, json.dumps(results, indent=4)), flush=True)    
    return
  

  def run_predict(self, text, timeit=True):
    """
    LABEL_0 = No offensive language
    LABEL_1 = Profanity (no directed insults)
    LABEL_2 = Insults (directed offensive language, lower level of offensiveness)
    
    LABEL_3 = Abuse (directed hate speech, racial slurs, sexist speech, threat with violence, death wishes, ..)        
    """
    start_time = time()
    # Tokenize the input text  
    inputs = self.__tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    
    for k, v in inputs.items():
      inputs[k] = v.to(self.__app_device)
    
    CLASSES = [
      "Limbaj non-ofensiv",
      "Limbaj vulgar (fara insulte directe)",
      "Insulte (limbaj ofensiv direct, nivel scazut de ofensivitate)",
      "Abuz (limbaj ofensiv direct, nivel ridicat de ofensivitate)"
    ]

      # Perform inference
    with th.no_grad():
      outputs = self.__model(**inputs)
      predictions = th.nn.functional.softmax(outputs.logits, dim=-1)
      predicted_class_id = predictions.argmax().item()

      
    # Return the prediction
    results = {
      "prediction": CLASSES[predicted_class_id],
      "metadata": {
        "version": __VER__,
        "worker" : self._local_id,
        "model": MODEL_NAME,
        "device" : str(predictions.device.type),
        "packages" : self.__packs_mandatory,
      }
    }

    if timeit:
      elapsed_time = time() - start_time
      self.__timings.append(elapsed_time)
      results['metadata']['elapsed_time'] = round(elapsed_time, 4)
      results['metadata']['average_time'] = round(np.mean(self.__timings), 4)

    return results   


eng = ModelHelper()

# Define the FastAPI app
app = FastAPI()

# Define the request body model
class Item(BaseModel):
  text: str

# FastAPI startup event
@app.on_event("startup")
async def startup_event():
  eng.build()
  return
  
    
    
@app.post("/predict/")
async def predict(item: Item):
  """
  Predict the classification of a given text sequence.

  Parameters
  ----------
  item : Item
      The input text for prediction.

  Returns
  -------
  JSONResponse
      The classification prediction result in JSON format.
      
  """
  # Tokenize the input text
  results = eng.run_predict(item.text)

  # Return the prediction
  return JSONResponse(content=results)