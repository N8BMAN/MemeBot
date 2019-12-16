# Author: Nathan Bowman <nate.bowman125@gmail.com>
#
# (C) Copyright 2018 by Nathan Bowman.  All Rights Reserved.

import discord
import logging
import asyncio
from discord.ext import commands
import traceback
from os import listdir
from os.path import isfile, join
import settings

settings.init()
meme = commands.Bot(description="Meme Bot is your God now", command_prefix=settings.config['General']['Prefix'])

cogs_dir = settings.config['General']['CogsDir']

@meme.event
async def on_ready():
  print("\nMeme-Bot Successfully Started!")
  print(f"Connected to {len(meme.guilds)} Servers.\n")
  
if __name__ == "__main__":
  meme.remove_command('help')
  for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
    if extension == '__init__': continue
    try:
      meme.load_extension(cogs_dir + "." + extension)
      print(f'Loaded extension \"{extension}\"')
    except Exception as e:
      print(f'Failed to load extension {extension}.')
      traceback.print_exc()

  try:
    meme.run(settings.config['General']['Token'])
  except discord.LoginFailure:
    input("Bot token incorrect. Update the ini file, then relaunch.")