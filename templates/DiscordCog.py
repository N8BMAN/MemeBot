import discord
from discord.ext import commands

class COGNAME(commands.Cog):
  def __init__(self, meme):
    self.meme = meme





def setup(meme):
  meme.add_cog(COGNAME(meme))