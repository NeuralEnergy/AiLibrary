# -*- coding: utf-8 -*-
"""
Chatbot (RO)

"""

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
    '--host_id', type=str,
    help='The host id'
  )
  
  args = parser.parse_args()
  host_id = args.host_id  

  l = Logger(
    "NEE",
    host_id=host_id,    
    base_folder='.', app_folder='_cache'
  )
  
  eng = TelegramChatbot(
    log=l, 
    bot_name='@neural_energy_bot',
    token_env_name='NEAIL_TELEGRAM_TOKEN', 
    persona='nee-sarcastic',
  )

  eng.run()