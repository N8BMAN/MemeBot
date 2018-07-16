# Author: Nathan Bowman <nate.bowman125@gmail.com>
#
# (C) Copyright 2018 by Nathan Bowman.  All Rights Reserved.

import discord
import logging
import asyncio
from discord.ext import commands
import traceback, configparser
from os import listdir
from os.path import isfile, join

configName = 'memebot.ini'
config = configparser.ConfigParser()
if(not isfile(configName)):
  config['General'] = {}
  config['General']['Token'] = input("Config file not found! Enter your bot token: ")
  config['General']['CogsDir'] = 'ext'
  config['General']['Prefix'] = '!'
  with open(configName, 'w') as configfile:
    config.write(configfile)
    configfile.close()
  print("Config file created...launching bot now\n")

with open(configName, 'r') as configfile:
  config.read_file(configfile)
token = config['General']['Token']
cogs_dir = config['General']['CogsDir']
prefix = config['General']['Prefix']
configfile.close()

meme = commands.Bot(description="Meme Bot is your God now", command_prefix=prefix)

@meme.event
async def on_ready():
  print("\nMeme-Bot Successfully Started!")
  x = 0
  for s in meme.servers:
    x = x+1
  print("Connected to "+str(x)+" Servers.\n")
  
@meme.command()
async def load(extension_name : str):
  """Loads other shit"""
  try:
    meme.load_extension(extension_name)
  except (AttributeError, ImportError) as e:
    await meme.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
    return
  await meme.say("{} loaded.".format(extension_name))
  
@meme.command()
async def unload(extension_name : str):
  """Unloads other shit"""
  meme.unload_extension(extension_name)
  await meme.say("{} unloaded.".format(extension_name))
  
if __name__ == "__main__":
  for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
    try:
      meme.load_extension(cogs_dir + "." + extension)
      print(f'Loaded extension \"{extension}\"')
    except Exception as e:
      print(f'Failed to load extension {extension}.')
      traceback.print_exc()

  try:
    meme.run(token)
  except discord.LoginFailure:
    config['General']['Token'] = input("Bot token incorrect! Enter your bot token then relaunch: ")
    with open(configName, 'w') as configfile:
      config.write(configfile)
      configfile.close()
    exit()