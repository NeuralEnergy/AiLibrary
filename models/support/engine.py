"""

Neural Energy Power Plant project 

@Author: Neuroplastic Software SRL
@Copyright: Neural Energy SRL
@description: Server monitoring module
@Date: 2022-12-04
@Last Modified by: Neuroplastic Software SRL




TODO:
  - revizuire si testarea endpoint /support_update_status pentru a asigura ca este 
    disponibil si functioneaza corect
    
  - adaugare analiza pe serie de timp a starii parametrilor de sistem
  
  - receptionare de la ingress gateway a tuturor serverelor existente si a 
    tuturor microserviciilor existente pentru a fi monitorizate
    
  - monitorizare individuala a fiecarui server si a fiecarui microserviciu (ping-uri periodice)

"""
import psutil

from models.support.base import BaseServerMonitor

__VERSION__ = '0.3.0'

class ServerMonitor(BaseServerMonitor):
  def __init__(self, **kwargs):
    super(ServerMonitor, self).__init__(**kwargs)
    self.__version__ = __VERSION__
    return
  
  def _collect_system_metrics(self, as_gb=True):
    """
    Collect system and application metrics including memory and disk usage.

    Parameters:
      as_gb (bool): Whether to return the metrics in GB.

    Returns:
      dict: Dictionary containing metrics about system and application.
    """
    metrics = {}
    
    # Conversion factor for bytes to GB
    to_gb = 1 if not as_gb else (1024 ** 3)
    
    # Memory Metrics
    memory_info = psutil.virtual_memory()
    metrics['total_memory'] = memory_info.total / to_gb
    metrics['available_memory'] = memory_info.available / to_gb
    metrics['system_used_memory'] = memory_info.used / to_gb
    metrics['app_used_memory'] = psutil.Process().memory_info().rss / to_gb
    
    # Disk Metrics
    disk_info = psutil.disk_usage('/')
    metrics['total_disk'] = disk_info.total / to_gb
    metrics['available_disk'] = disk_info.free / to_gb
    
    return metrics

    
