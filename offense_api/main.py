import json
import torch as th
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from time import time
import pkg_resources

CACHE_DIR = './_models_cache'
MODEL_NAME = "readerbench/ro-offense"

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
    self.model_name = model_name
    self.cache_dir = cache_dir
    self.tokenizer = None
    self.model = None
    self.app_device = None
    self.__packs = None
    return
  
  def P(self, s, **kwargs):
    print(s, flush=True)
    return
  
  def __init(self):
    self.P("Initializing model helper ...", flush=True)
    self.__packs = get_packages()
    self.P("Packages: \n{}".format("\n".join(self.__packs)), flush=True)
    return
  
  
  def build(self):
    self.P("Building model helper ...")
    self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir)
    self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, cache_dir=self.cache_dir)
    if th.cuda.is_available():
      self.app_device = th.device('cuda:0')
    else:
      self.app_device = th.device('cpu')
    self.model = self.model.to(self.app_device)
    
    if th.cuda.is_available():
      self.P("GPU: {}".format(th.cuda.get_device_name(0)), flush=True) 
    else:
      self.P("GPU: Not available", flush=True)
    
    WARMUP_TEXT = "Esti destept!"
    results = self.run_predict(text=WARMUP_TEXT)
    self.P("Warmup on '{}': {}".format(WARMUP_TEXT, json.dumps(results, indent=4)), flush=True)    
    return
  

  def run_predict(self, text):
    """
    LABEL_0 = No offensive language
    LABEL_1 = Profanity (no directed insults)
    LABEL_2 = Insults (directed offensive language, lower level of offensiveness)
    
    LABEL_3 = Abuse (directed hate speech, racial slurs, sexist speech, threat with violence, death wishes, ..)        
    """
    start_time = time()
    # Tokenize the input text  
    inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    
    for k, v in inputs.items():
      inputs[k] = v.to(self.app_device)
    
    CLASSES = [
      "No offensive language",
      "Profanity (no directed insults)",
      "Insults (directed offensive language, lower level of offensiveness)",
      "Abuse (directed hate speech, racial slurs, sexist speech, threat with violence, death wishes, ..)"
    ]

      # Perform inference
    with th.no_grad():
      outputs = self.model(**inputs)
      predictions = th.nn.functional.softmax(outputs.logits, dim=-1)
      predicted_class_id = predictions.argmax().item()

    elapsed_time = time() - start_time
    # Return the prediction
    results = {
      "prediction": CLASSES[predicted_class_id],
      "metadata": {
        "model": "readerbench/ro-offense",
        "device" : str(predictions.device.type),
        "elapsed_time": elapsed_time,
      }
    }
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