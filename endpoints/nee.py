# -*- coding: utf-8 -*-
"""
Copyright (C) 2017-2021 Andrei Damian, andrei.damian@me.com,  All rights reserved.

This software and its associated documentation are the exclusive property of the creator.
Unauthorized use, copying, or distribution of this software, or any portion thereof,
is strictly prohibited.


Dissemination of this information or reproduction of this material is strictly forbidden unless prior
written permission from the author

"""
__VER__ = '1.1.4'

import numpy as np
import os
import sys
import traceback
cwd = os.getcwd()
print("{} running from: {}".format(__file__, cwd), flush=True)
sys.path.append(cwd)


FULL_DEBUG = False

# from typing import Final
# TOKEN: Final = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# BOT_USERNAME: Final = '@neural_energy_bot'

DATA_CACHE = {
  'log'         : None,
  'engine'      : None,
  'bot_token'   : os.environ['TELEGRAM_TOKEN'],
  'bot_name'    : '@neural_energy_bot',
}


from basic_inference_server import Logger
from models.api.app import OpenAIApp



# pip install python-telegram-bot
from telegram import Update, Message
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

def _log_print(s, color=None):
  DATA_CACHE['log'].P(s, color=color)



# Lets us use the /start command
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#   await update.message.reply_text(
#     'Salut! Sunt un robot conversational care invata. Sistemul meu de AI este dezvoltat printr-un grant de finantare aferent proiectului „Mobile Neural Powerplant” – cod SMIS 156244. Acest proiect este finanțat în cadrul Programului Operational Competitivitate 2014-2020, Componenta 1: Întreprinderi inovatoare de tip start-up si spin-off - Apel 2022, Axa Prioritară: Cercetare, dezvoltare tehnologica si inovare (CDI) în sprijinul competitivitatii economice si dezvoltarii afacerilor, Operatiunea: Stimularea cererii întreprinderilor pentru inovare prin proiecte CDI derulate de întreprinderi individual sau în parteneriat cu institute de CD si universitati, în scopul inovarii de procese si de produse în sectoarele economice care prezinta potential de crestere. In cadrul acestui proiect lucreaza mentorul meu iar pe cheama Nee, cu ce te pot ajuta?'
#   )


# # Lets us use the /help command
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#   await update.message.reply_text('Scrie ceva si voi incerca sa te ajut...')


# # Lets us use the /custom command
# async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#   await update.message.reply_text('Comanda custom neimplementata momentan. Reveniti dupa ce mai invat...')


def handle_response(user: str, text: str) -> str:
  
  _log_print("  Preparing response for {}...".format(user))
  
  # Create your own response logic
  processed: str = text.lower()
  
  eng : OpenAIApp = DATA_CACHE['engine']
  
  answer = eng.ask(question=processed, user=str(user))

  return answer


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  message : Message = update.message
  if message is None:
    return
  # Get basic info of the incoming message
  message_type: str = message.chat.type
  text: str = message.text
  bot_name : str = DATA_CACHE['bot_name']
  
  
  initiator_id = message.from_user.id
  if message.from_user.first_name is not None:
    initiator_name = message.from_user.first_name
  else:
    initiator_name = initiator_id

  is_bot_in_text = bot_name in text
  text = text.replace(bot_name , '').strip()
  chat_name = message.chat.title
  
  if FULL_DEBUG:
    _log_print(f'User {initiator_name} ({initiator_id}) in `{chat_name}` ({message_type}): "{text}"')
  
  allow = False
  # React to group messages only if users mention the bot directly
  if message_type in ['group', 'supergroup']:
    if is_bot_in_text:
      allow = True
    else:
      reply_to = message.reply_to_message
      if reply_to is not None:
        _log_print(f"Reply from '{initiator_name}' to {reply_to.from_user} ")
        if reply_to.from_user.is_bot:
          allow = True
  else:
    chat_name = initiator_name
    allow = True
  
  if not allow:
    return

  if not FULL_DEBUG:
    # Print a log for debugging
    _log_print(f'User {initiator_name} ({initiator_id}) in `{chat_name}` ({message_type}): "{text}"')
  
  response: str = handle_response(user=initiator_id, text=text)

  # Reply normal if the message is in private
  _log_print('  Bot resp: {}'.format(response), color='m')
  await message.reply_text(response)
  return


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
  exc = traceback.format_exc()
  _log_print(f'Update {update} caused error {context.error}\n\nChat data:{context.chat_data}\n\nUser data:{context.user_data}\n\nTrace:{exc}', color='r')
  return

  
if __name__ == '__main__':
  l = Logger("NEEBOT", base_folder='.', app_folder='_cache')
  eng = OpenAIApp(
    persona='nee-sarcastic',
    user=None,
    log=l,
    persona_location='./models/personas/',
  )
  DATA_CACHE['log'] = l
  DATA_CACHE['engine'] = eng
  bot_token = DATA_CACHE['bot_token']
  

  msg = "*   Starting [Telegram] '{}' bot v{} {}...   *".format(DATA_CACHE['bot_name'], __VER__, bot_token)
  l.P('*' * len(msg), color='g')
  l.P('*' + ' ' * (len(msg) - 2) + '*', color='g')
  l.P(msg, color='g')
  l.P('*' + ' ' * (len(msg) - 2) + '*', color='g')
  l.P('*' * len(msg), color='g')
  app = Application.builder().token(bot_token).build()

  # Commands
  # app.add_handler(CommandHandler('start', start_command))
  # app.add_handler(CommandHandler('help', help_command))
  # app.add_handler(CommandHandler('custom', custom_command))

  # Messages
  app.add_handler(MessageHandler(filters.TEXT, handle_message))

  # Log all errors
  app.add_error_handler(error)

  l.P('Polling...')
  # Run the bot
  app.run_polling(poll_interval=3)  