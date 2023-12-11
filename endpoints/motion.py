import os
import sys
import argparse
cwd = os.getcwd()
print("{} running from: {}".format(__file__, cwd), flush=True)
sys.path.append(cwd)


from models.telegram.base_engine import TelegramChatbot
from basic_inference_server import Logger

  
  
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
  
  l = Logger(
    "MO", 
    host_id=host_id,
    base_folder='.', app_folder='_cache'
  )
  
  if l.app_debug_mode:
    l.P("App is running in debug mode - chatbot disabled", color='r', boxed=True)
  else:
    eng = TelegramChatbot(
      log=l, 
      bot_name='@Motionmask_bot',
      token_env_name='NEAIL_MOTION_TOKEN', 
      persona='motionmask-funny',
    )
    eng.run() 