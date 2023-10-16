# -*- coding: utf-8 -*-
"""
Prezentare (RO): 
  - modul de analiza paralela a intregului ecosystem de servere
  - ecosystemul de servere este compus dintr-un server the tip "ingress gateway" care va ridica servere individuale pentru fiecare microserviciu in acelasi container
  - fiecare microserviciu este un server de tip "model server" care va rula un model de invatare automata (profunda sau superficiala) cu logica si euristici 
  - modulele de tp "support" sunt module care nu au un server dedicat, dar care pot fi folosite pentru a monitoriza starea serverelor si a microserviciilor
  - fiecare modul de tip "support" va accesa un endpoint dedicat `/support_update_status` de tip "support" care este disponibil pe serverul de tip gateway
  
TODO:
  - revizuire si testarea endpoint /support_update_status pentru a asigura ca este disponibil si functioneaza corect
  - adaugare analiza pe serie de timp a starii parametrilor de sistem
  - receptionare de la ingress gateway a tuturor serverelor existente si a tuturor microserviciilor existente pentru a fi monitorizate
  - monitorizare individuala a fiecarui server si a fiecarui microserviciu (ping-uri periodice)

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

__VERSION__ = '0.2.1'

class ServerMonitor:
  def __init__(self, name, log, interval=None, debug=False, use_gb=True):
    self.log = log
    self.use_gb = use_gb  
    self.__debug = debug
    self.__name = name
    if interval is None:
      interval = self.log.config_data.get('PING_INTERVAL', 1)
    self.__interval = interval
    self.__run_cnt = 0
    self.__server = self.log.config_data['SERVER']
    self.__port = self.log.config_data['SERVER_PORT']
    self.__path = self.log.config_data['SERVER_PATH']
    self.P("ServerMonitor v{} initialized on {}s interval".format(__VERSION__, self.__interval))
    self.P("  Delay for service sync...")
    sleep(10)
    self.P("  Delay done, syncronizing with gateway...")
    return
  
  def P(self, s, color='m'):
    self.log.P(s, color=color)
    return

  def _collect_system_metrics(self):
    """Collect system metrics like memory and disk usage"""
    
    metrics = {}
    
    # Memory metrics
    memory = psutil.virtual_memory()
    metrics['memory'] = {
      'total': self.log.get_machine_memory(gb=self.use_gb),
      'used': memory.used / (1024 ** 3) if self.use_gb else memory.used,
      'free': self.log.get_avail_memory(gb=self.use_gb),
    }
    
    # Disk metrics
    disk = psutil.disk_usage('/')
    metrics['disk'] = {
      'total': disk.total / (1024 ** 3) if self.use_gb else disk.total,
      'used': disk.used / (1024 ** 3) if self.use_gb else disk.used,
      'free': disk.free / (1024 ** 3) if self.use_gb else disk.free
    }
    
    # CPU metrics
    cpu_percent = psutil.cpu_percent()
    cpu_percent_per_core = psutil.cpu_percent(percpu=True)
    metrics['cpu'] = {
      'total_percent': cpu_percent,
      'percent_per_core': cpu_percent_per_core
    }
    
    return metrics

  
  def _send_data(self, data):
    url = None
    try:
      assert isinstance(data, dict)
      url = 'http://{}:{}{}'.format(
        self.__server,
        self.__port,
        self.__path,
      )
      data['SIGNATURE'] = self.__name
      if self.__debug:
        self.P("Sending data to {}".format(url), color='m')
      r = requests.post(url, json=data)
      if self.__debug:
        self.P("Response: {}".format(r.text), color='m')
    except Exception as e:
      self.P("Error while sending to {}: {}:\n{}".format(url, e, json.dumps(data, indent=2)), color='r')
    return
      
      
    
  def execute(self):        
    metrics = self._collect_system_metrics()    
    msg = (
      "T.Mem: {:.1f}GB, U.Mem: {:.1f}GB, F.Mem: {:.1f}GB, "
      "T.Disk: {:.1f}GB, U.Disk: {:.1f}GB, F.Disk: {:.1f}GB, "
      "T.CPU: {:.1f}%, Cores: {}, C:{}"
    ).format(
      metrics['memory']['total'], metrics['memory']['used'], metrics['memory']['free'],
      metrics['disk']['total'], metrics['disk']['used'], metrics['disk']['free'],
      metrics['cpu']['total_percent'], metrics['cpu']['percent_per_core'],
      self.__run_cnt,
    )

  
    data = dict(
      run_count=self.__run_cnt,
      **metrics,            
    )
    if (self.__run_cnt % 50 == 0):
      data['msg'] = msg
    self._send_data(data)
    self.__run_cnt += 1
    return

  def run(self):
    tick = time()
    while True:
      self.execute()
      while (time() - tick) < self.__interval:
        sleep(0.1)
      tick = time()
    return
      
    

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  
  parser.add_argument(
    '--config_endpoint', type=str, default='{}',
    help='JSON configuration of the endpoint'
  )
  
  args = parser.parse_args()
  str_config_data = args.config_endpoint
  print("Using --config_endpoint: {}".format(str_config_data))
  config_data = json.loads(str_config_data)
  name = config_data.get("SUPPORT_NAME", "SUPPORT")
  
  log = Logger(
    lib_name="SPRC",
    base_folder=".",
    app_folder="_cache",
    TF_KERAS=False, # use_tf
    max_lines=3000
  )  
  
  log.update_config_data(config_data)
  
  
  log.P("Using config_data: \n{}".format(json.dumps(log.config_data, indent=2)))
  
  engine = ServerMonitor(name=name, log=log) 
  engine.run()

