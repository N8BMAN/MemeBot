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

@meme.command()
async def listCogs(ctx):
  message = '**Extensions Currently Running:**\n'
  for ext in meme.extensions:
    message+=f'{ext[4:]}\n'
  await ctx.send(message)
  
@meme.command()
async def load(ctx, extension_name : str):
  """Loads other shit"""
  try:
    meme.load_extension(cogs_dir + '.' + extension_name)
  except (AttributeError, ImportError) as e:
    await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
    return
  await ctx.send(f"Extension **{extension_name}** loaded.")
  
@meme.command()
async def unload(ctx, extension_name : str):
  """Unloads other shit"""
  meme.unload_extension(cogs_dir + '.' + extension_name)
  await ctx.send(f"Extension **{extension_name}** unloaded.")
  
if __name__ == "__main__":
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