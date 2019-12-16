import discord
import sys
from discord.ext import commands
from os.path import isfile, join
from os import listdir
from settings import config
from ext.sounds import Sounds

class Meta(commands.Cog):
  def __init__(self, meme):
    self.meme = meme

  async def allCommands(self, ctx):
    embed=discord.Embed(title="Meme Bot Commands", color=discord.Color.magenta())
    embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/419337073779015720/736339f7c969c405b4ecd15de50cfb04.png?size=512")
    embed.set_footer(text="Don't @ Me")

    cogs = self.meme.cogs
    for cog in cogs:
      if cog == "Sounds":
        embed.add_field(name=cog, value="\u2022 help Sounds \u21e8 List all available sound clips")
      else:
        commands = dict(zip([cmd.name for cmd in cogs[cog].get_commands()], [cmd.help for cmd in cogs[cog].get_commands()]))
        if len(commands) == 0:
          continue
        value = [f"\u2022 {name}: \u21e8 {commands[name]}" for name in commands]
        embed.add_field(name=cog, value="\n".join(value), inline=False)
    await ctx.send(embed=embed)

  async def soundCommands(self, ctx):
    embed=discord.Embed(title="Meme Bot Commands", color=discord.Color.magenta())
    embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/419337073779015720/736339f7c969c405b4ecd15de50cfb04.png?size=512")
    embed.set_footer(text="Don't @ Me")

    sounds = (await Sounds.getSoundDictionary()).keys()
    value = [f"\u2022 {sound}" for sound in sounds]
    embed.add_field(name="Sound Commands:", value="\n".join(value), inline=False)
    await ctx.send(embed=embed)

  @commands.command()
  async def help(self, ctx, cog=None):
    '''Shows this message'''
    if cog == "Sounds":
      await self.soundCommands(ctx)
    else:
      await self.allCommands(ctx)

  @commands.command()
  async def listCogs(self, ctx):
    """List other shit"""
    message = '**Extensions Currently Running:**\n'
    for ext in self.meme.extensions:
      message+=f'{ext[4:]}\n'
    await ctx.send(message)
    
  @commands.command()
  async def load(self, ctx, extension_name : str):
    """Loads other shit"""
    try:
      self.meme.load_extension(config['General']['CogsDir'] + '.' + extension_name)
    except (AttributeError, ImportError) as e:
      await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
      return
    await ctx.send(f"Extension **{extension_name}** loaded.")
    
  @commands.command()
  async def unload(self, ctx, extension_name : str):
    """Unloads other shit"""
    self.meme.unload_extension(config['General']['CogsDir'] + '.' + extension_name)
    await ctx.send(f"Extension **{extension_name}** unloaded.")

  @commands.command()
  async def reload(self, ctx, extension_name : str):
    """Reloads other shit"""
    self.meme.reload_extension(config['General']['CogsDir'] + '.' + extension_name)
    await ctx.send(f"Extension **{extension_name}** unloaded.")

def setup(meme):
  meme.add_cog(Meta(meme))