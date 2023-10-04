# -*- coding: utf-8 -*-
"""
Copyright (C) 2017-2021 Andrei Damian, andrei.damian@me.com,  All rights reserved.

This software and its associated documentation are the exclusive property of the creator.
Unauthorized use, copying, or distribution of this software, or any portion thereof,
is strictly prohibited.


Dissemination of this information or reproduction of this material is strictly forbidden unless prior
written permission from the author

"""
__VER__ = '0.2.3'

import numpy as np
import os
import sys
cwd = os.getcwd()
print("{} running from: {}".format(__file__, cwd), flush=True)
sys.path.append(cwd)

from time import sleep

# from typing import Final
# TOKEN: Final = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# BOT_USERNAME: Final = '@neural_energy_bot'

DATA_CACHE = {
  'log'   : None,
  'bot_token' : os.environ['TELEGRAM_TOKEN'],
  'bot_name'   : '@neural_energy_bot',
}

WORKING = [
  'Pregatesc raspunsul...',
  'Lucrez la raspuns...',
  'Muncesc, putin rabdare',
  'Imediat revin...',
  'Incerc acum sa inteleg...',
  'Putin rabdare, revin',
  'Doua secunde te rog, cum ar spune mentorul meu',
  'Imediat sa vad ce pot raspunde...',
  'Revin mintenas',
  'Stai 2 secunde ...',
  'In lucru acum cu raspunsul tau...',
  'Acum, acum, revin numaidecat...',
  'Stai sa ma gandesc...',
  'Procesez :) ...',
  'Hmmm....'
]

from basic_inference_server import Logger



# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

def _log_print(s, color=None):
  DATA_CACHE['log'].P(s, color=color)



# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text(
    'Salut! Sunt un robot conversational care invata. Sistemul meu de AI este dezvoltat printr-un grant de finantare aferent proiectului „Mobile Neural Powerplant” – cod SMIS 156244. Acest proiect este finanțat în cadrul Programului Operational Competitivitate 2014-2020, Componenta 1: Întreprinderi inovatoare de tip start-up si spin-off - Apel 2022, Axa Prioritară: Cercetare, dezvoltare tehnologica si inovare (CDI) în sprijinul competitivitatii economice si dezvoltarii afacerilor, Operatiunea: Stimularea cererii întreprinderilor pentru inovare prin proiecte CDI derulate de întreprinderi individual sau în parteneriat cu institute de CD si universitati, în scopul inovarii de procese si de produse în sectoarele economice care prezinta potential de crestere. In cadrul acestui proiect lucreaza mentorul meu iar pe cheama Nee, cu ce te pot ajuta?'
  )


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('Scrie ceva si voi incerca sa te ajut...')


# Lets us use the /custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('Comanda custom neimplementata momentan. Reveniti dupa ce mai invat...')


def handle_response(text: str) -> str:
  
  _log_print("  Preparing response ...")
  sleep(2)
  
  # Create your own response logic
  processed: str = text.lower()

  if any(tag in processed for tag in ['salut', 'buna', 'servus']):
    return np.random.choice([
      'Buna!', 'Servus!', 'Salutare!', 'Salut!'
    ])

  if any(tag in processed for tag in ['ce faci', 'cum esti', 'simti']):
    return np.random.choice([
      'Eu sunt bine! Tu?', 'Eu ma simt excelent!', 'Sunt pe cai mari! Sper ca si tu!', 'Ma simt nemaipomenit!', 'Nemaivazut :)'
    ])

  if any(tag in processed for tag in ['ajut', 'limit', 'sprijin']):
    return np.random.choice([
      'Momentan sunt foarte limitat si inca invat cum sa pot ajuta. Vino mai tarziu...', 
      'Nu te pot ajuta cu prea multe... sunt inca foarte limitat', 
      'Momentan sunt limitat la script-uri destul de simple... scuze', 
      'As vrea sa te pot ajuta si sprijini mai mult dar mentorul meu inca nu mi-a incarcat motorul neural ...'
    ])

  miss = np.random.choice([
    'Imi pare rau dar nu inteleg "{}". Inca acumulez informatii si invat ...'.format(text),
    'Nee nu a inteles ce vrei sa spui cu "{}", Nee inca invata... nu e usor sa inveti'.format(text),
    'Ma voi ocupa sa inteleg ce inseamna "{}". Momentan nu inteleg'.format(text),  
  ])
  return miss


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
  await update.message.reply_text(np.random.choice(WORKING))
  
  response: str = handle_response(text)

  # Reply normal if the message is in private
  _log_print('  Bot resp: {}'.format(response), color='m')
  await update.message.reply_text(response)
  return


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
  _log_print(f'Update {update} caused error {context.error}', color='r')

  
if __name__ == '__main__':
  l = Logger("TELBOT", base_folder='.', app_folder='_cache')
  DATA_CACHE['log'] = l
  bot_token = DATA_CACHE['bot_token']

  msg = "*   Starting [Telegram] '{}' bot v{} {}...   *".format(DATA_CACHE['bot_name'], __VER__, bot_token)
  l.P('*' * len(msg), color='g')
  l.P('*' + ' ' * (len(msg) - 2) + '*', color='g')
  l.P(msg, color='g')
  l.P('*' + ' ' * (len(msg) - 2) + '*', color='g')
  l.P('*' * len(msg), color='g')
  app = Application.builder().token(bot_token).build()

  # Commands
  app.add_handler(CommandHandler('start', start_command))
  app.add_handler(CommandHandler('help', help_command))
  app.add_handler(CommandHandler('custom', custom_command))

  # Messages
  app.add_handler(MessageHandler(filters.TEXT, handle_message))

  # Log all errors
  app.add_error_handler(error)

  l.P('Polling...')
  # Run the bot
  app.run_polling(poll_interval=3)  