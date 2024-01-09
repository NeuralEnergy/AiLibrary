"""

Neural Energy Power Plant project 

@Author: Neuroplastic Software SRL
@Copyright: Neural Energy SRL
@description: Server monitoring module
@Date: 2022-12-04
@Last Modified by: Neuroplastic Software SRL


"""
import psutil

from models.support.base import BaseServerMonitor

__VERSION__ = '0.4.1'

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
    metrics['total_mem'] = round(memory_info.total / to_gb, 2)
    metrics['avail_mem'] = round(memory_info.available / to_gb, 2)
    metrics['sys_used_mem'] = round(memory_info.used / to_gb, 4)
    metrics['app_used_mem'] = round(psutil.Process().memory_info().rss / to_gb, 4)
    
    # Disk Metrics
    disk_info = psutil.disk_usage('/')
    metrics['total_disk'] = round(disk_info.total / to_gb, 2)
    metrics['avail_disk'] = round(disk_info.free / to_gb, 2)
    
    metrics['GiB'] = as_gb
    
    return metrics

    
