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

token = "NDE5MzM3MDczNzc5MDE1NzIw.Da1noQ.zDne822BF3sKIJajt4S9lCjfhAc"
cogs_dir = "ext"

people = {"189495247762489344", "196139912020492289", "226455807300993024", "321871570144329728", "196798817054490624", "405947141396103168", "179706306586738688"}
#                   Me                        Emilio                        Dunkey                      LitRoom                   Caleb                         Jack                        Armand

meme = commands.Bot(description="Meme Bot is your God now", command_prefix="!")

print("DON'T CLOSE THIS SHIT")

@meme.event
async def on_ready():
  print("Meme-Bot Successfully Started!")
  x = 0
  for s in meme.servers:
    x = x+1
  print("Connected to "+str(x)+" Servers.")
  
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
    print("Incorrect token! Plz fix!")