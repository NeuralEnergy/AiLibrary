"""

Neural Energy Power Plant project 

@Author: Neuroplastic Software SRL
@Copyright: Neural Energy SRL
@description: Server monitoring module - base class
@Date: 2022-12-04
@Last Modified by: Neuroplastic Software SRL

  
  
"""
import numpy as np
import requests
from collections import deque

from time import time, sleep

__SUPPORT_PROCESS_VERSION__ = '0.0.0'

class BaseServerMonitor:
  def __init__(self, name, log, interval=None, debug=False):
    self.__version__ = __SUPPORT_PROCESS_VERSION__
    self.log = log
    self.__debug = debug
    self.__name = name
    self.__timeseries = {}
    self.__counts = {}
    if interval is None:
      interval = self.log.config_data.get('PING_INTERVAL', 1)
    self.__interval = interval
    self.__run_cnt = 0
    self.__server = self.log.config_data['SERVER']
    self.__port = self.log.config_data['SERVER_PORT']
    self.__path = self.log.config_data['SERVER_PATH']
    self.P("ServerMonitor v{} initialized on {}:{}{} at {}s interval".format(
      self.__version__, self.__server, self.__port, self.__path, self.__interval
      ), color='g', boxed=True
    )
    return
  
  def P(self, s, color=None, boxed=False):
    self.log.P(s, color=color, boxed=boxed)
    return

  def _collect_system_metrics(self, as_gb=True):
    """
    Collect system and application metrics including memory and disk usage.

    Parameters:
      as_gb (bool): Whether to return the metrics in GB.

    Returns:
      dict: Dictionary containing metrics about system and application.
    """
    raise NotImplementedError("Must be implemented by subclass")
  
  
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
      self.P("Error while trying to deliver to {}: {}".format(url, e), color='r')
    return
      
  def _register_metrics(self, metrics):
    """
    Register the metrics to be collected by the monitoring service.
    """
    dct_results = {}
    for k, v in metrics.items():
      if k not in self.__timeseries:
        self.__timeseries[k] = deque(maxlen=10_000)
      self.__timeseries[k].append(v)
      self.__counts[k] = self.__counts.get(k, 0) + 1
      if len(self.__timeseries[k]) > 1 and isinstance(v, (int, float)):
        key1 = k + '_mean'
        dct_results[key1] = round(np.mean(self.__timeseries[k]), 3)
        key2 = k + '_count'
        dct_results[key2] = "{}/{}".format(
          self.__counts[k],
          len(self.__timeseries[k]),
        )
        key3 = k + '_min'
        dct_results[key3] = round(np.min(self.__timeseries[k]), 3)
        key4 = k + '_max'
        dct_results[key4] = round(np.max(self.__timeseries[k]), 3)
    return dct_results
      
    
  def execute(self):    
    self.__run_cnt += 1
    metrics = self._collect_system_metrics()
    metrics['statistics'] = self._register_metrics(metrics)
    str_msg = "{} v{} ".format(self.__name, self.__version__)
    
    dct_msg = {
      'msg' : str_msg,
      **metrics,
    }
  
    data = dict(
      data=dct_msg,
      **metrics,      
    )
    self._send_data(data)
    return

  def run(self):
    tick = time()
    while True:
      while (time() - tick) < self.__interval:
        sleep(0.1)
      self.execute()
      tick = time()
    return
      
    
