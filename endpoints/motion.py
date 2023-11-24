import os
import sys
cwd = os.getcwd()
print("{} running from: {}".format(__file__, cwd), flush=True)
sys.path.append(cwd)

from models.telegram.base_engine import BaseEngine
from basic_inference_server import Logger

  
if __name__ == '__main__':
  l = Logger("MOTION", base_folder='.', app_folder='_cache')
  
  eng = BaseEngine(
    log=l, 
    bot_name='@Motionmask_bot',
    token_env_na='MOTION_TOKEN', 
    persona='motionmask-funny',
  )

  eng.run() 