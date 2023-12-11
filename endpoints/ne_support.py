# -*- coding: utf-8 -*-
"""
Prezentare (RO): 
  - modul de analiza paralela a intregului ecosystem de servere
  - ecosystemul de servere este compus dintr-un server the tip "ingress gateway" care va ridica servere individuale pentru fiecare microserviciu in acelasi container
  - fiecare microserviciu este un server de tip "model server" care va rula un model de invatare automata (profunda sau superficiala) cu logica si euristici 
  - modulele de tp "support" sunt module care nu au un server dedicat, dar care pot fi folosite pentru a monitoriza starea serverelor si a microserviciilor
  - fiecare modul de tip "support" va accesa un endpoint dedicat `/support_update_status` de tip "support" care este disponibil pe serverul de tip gateway
"""

import json
import datetime
import argparse
import requests
import psutil
import os
import sys
cwd = os.getcwd()
print("{} running from: {}".format(__file__, cwd), flush=True)
sys.path.append(cwd)

from time import sleep, time

from basic_inference_server import Logger
from models.support.engine import ServerMonitor


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  
  parser.add_argument(
    '--config_endpoint', type=str, default='{}',
    help='JSON configuration of the endpoint'
  )
  
  parser.add_argument(
    '--host_id', type=str,
    help='The host id'
  )
  
  args = parser.parse_args()
  host_id = args.host_id
  
  str_config_data = args.config_endpoint
  print("Using --config_endpoint: {}".format(str_config_data))
  config_data = json.loads(str_config_data)
  name = config_data.get("SUPPORT_NAME", "SUPPORT")
  
  log = Logger(
    lib_name="SPRC",
    host_id=host_id,
    base_folder=".",
    app_folder="_cache",
    TF_KERAS=False, # use_tf
    max_lines=3000
  )  
  
  log.update_config_data(config_data)
  
  
  log.P("Using config_data: \n{}".format(json.dumps(log.config_data, indent=2)))
  
  engine = ServerMonitor(name=name, log=log) 
  engine.run()

