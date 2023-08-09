# -*- coding: utf-8 -*-
"""
Copyright (C) 2017-2021 Andrei Damian, andrei.damian@me.com,  All rights reserved.

This software and its associated documentation are the exclusive property of the creator.
Unauthorized use, copying, or distribution of this software, or any portion thereof,
is strictly prohibited.

Parts of this software are licensed and used in software developed by Lummetry.AI.
Any software proprietary to Knowledge Investment Group SRL is covered by Romanian and  Foreign Patents,
patents in process, and are protected by trade secret or copyright law.

Dissemination of this information or reproduction of this material is strictly forbidden unless prior
written permission from the author


@copyright: Lummetry.AI
@author: Lummetry.AI
@project: 
@description:
@created on: Tue Aug  8 18:03:44 2023
@created by: damia
"""
__VER__ = '0.2.0'

import numpy as np
import os
import sys
cwd = os.getcwd()
sys.path.append(cwd)

from time import sleep

DATA_CACHE = {
  'log' : None,
  
}

from basic_inference_server import Logger

from typing import Final

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

def _log_print(s, color=None):
  DATA_CACHE['log'].P(s, color=color)

TOKEN: Final = '6083297729:AAGIoXdzzESoewpBVWOUKdCqwG0dXMs-21M'
BOT_USERNAME: Final = '@neural_energy_bot'


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('Salut! Sunt un robot conversational care invata. Ma cheama Nee, cu ce te pot ajuta?')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('Scrie ceva si voi incerca sa te ajut...')


# Lets us use the /custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text('Comanda custom neimplementata momentan. Reveniti dupa ce mai invat...')


def handle_response(text: str) -> str:
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

  # Print a log for debugging
  _log_print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

  # React to group messages only if users mention the bot directly
  if message_type == 'group':
    # Replace with your bot username
    if BOT_USERNAME in text:
      new_text: str = text.replace(BOT_USERNAME, '').strip()
      response: str = handle_response(new_text)
    else:
      return  # We don't want the bot respond if it's not mentioned in the group
  else:
    response: str = handle_response(text)

  # Reply normal if the message is in private
  _log_print('  Bot resp: {}'.format(response), color='m')
  await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
  _log_print(f'Update {update} caused error {context.error}', color='r')

  
if __name__ == '__main__':
  l = Logger("TELBOT", base_folder='.', app_folder='_cache')
  l.P("Starting up Telegram bot v{}...".format(__VER__))
  DATA_CACHE['log'] = l
  
  app = Application.builder().token(TOKEN).build()

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