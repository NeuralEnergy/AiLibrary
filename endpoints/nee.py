# -*- coding: utf-8 -*-
"""
Copyright (C) 2017-2021 Andrei Damian, andrei.damian@me.com,  All rights reserved.

This software and its associated documentation are the exclusive property of the creator.
Unauthorized use, copying, or distribution of this software, or any portion thereof,
is strictly prohibited.


Dissemination of this information or reproduction of this material is strictly forbidden unless prior
written permission from the author

"""
__VER__ = '1.0.3'

import numpy as np
import os
import sys
cwd = os.getcwd()
print("{} running from: {}".format(__file__, cwd), flush=True)
sys.path.append(cwd)


# from typing import Final
# TOKEN: Final = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# BOT_USERNAME: Final = '@neural_energy_bot'

DATA_CACHE = {
  'log'         : None,
  'engine'      : None,
  'bot_token'   : os.environ['MOTION_TOKEN'],
  'bot_name'    : '@neural_energy_bot',
}


from basic_inference_server import Logger
from models.api.app import OpenAIApp



# pip install python-telegram-bot
from telegram import Update
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
  # Get basic info of the incoming message
  message_type: str = update.message.chat.type
  text: str = update.message.text
  
  initiator_id = update.message.from_user.id
  if update.message.from_user.first_name is not None:
    initiator_name = update.message.from_user.first_name
  else:
    initiator_name = initiator_id
  
  # React to group messages only if users mention the bot directly
  if message_type == 'group':
    # Replace with your bot username
    if DATA_CACHE['bot_name'] in text:
      text = text.replace(DATA_CACHE['bot_name'] , '').strip()
      chat_name = update.message.chat.title
    else:
      return  # We don't want the bot respond if it's not mentioned in the group
  else:
    chat_name = initiator_name

  # Print a log for debugging
  _log_print(f'User {initiator_name} ({initiator_id}) in "{chat_name}"({message_type}): "{text}"')
  
  response: str = handle_response(user=initiator_id, text=text)

  # Reply normal if the message is in private
  _log_print('  Bot resp: {}'.format(response), color='m')
  await update.message.reply_text(response)
  return


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
  _log_print(f'Update {update} caused error {context.error}', color='r')

  
if __name__ == '__main__':
  l = Logger("MOTION", base_folder='.', app_folder='_cache')
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