import discord
import sys
from discord.ext import commands
from os.path import isfile, join
from os import listdir
from settings import config
from gtts import gTTS
from io import BytesIO
from tempfile import TemporaryFile

class Sounds(commands.Cog):
  '''!help Sounds to see available sound clips'''
  def __init__(self, meme):
    self.meme = meme

  async def connectForSound(self, member, f):
    '''Connects to the voice channel the given member is in, and plays the given file'''
    commands.HelpCommand()
    if(isfile(join(config['Sounds']['ClipsDir'], f))):
      if(member.voice.channel):
        voice = await member.voice.channel.connect()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(join(config['Sounds']['ClipsDir'], f)))
        voice.play(source)
        while(voice.is_playing()): None
        await voice.disconnect()
    else:
      print("N8 fucked up the file name")

  @staticmethod
  async def getAllSoundFiles():
    '''Returns the list of all files found in the configured sound clips directory'''
    return [f for f in listdir(config['Sounds']['ClipsDir']) if isfile(join(config['Sounds']['ClipsDir'], f))]

  @staticmethod
  async def getSoundDictionary():
    '''Returns the dictionary of all sound clips and their file names'''
    files = await Sounds.getAllSoundFiles()
    return dict(zip([key.split(".")[0] for key in files], files))

  @commands.command()
  async def playSound(self, ctx, clip):
    '''!help Sounds to see a list of clips'''
    soundsDict = await Sounds.getSoundDictionary()
    if clip in soundsDict:
      await Sounds.connectForSound(self, ctx.message.author, soundsDict[clip])
    else:
      await ctx.send("Sound clip not found. Try again.")

  @commands.command()
  async def say(self, ctx, *, script):
    '''Meme-Bot Talks! Tell him what to say'''
    try:
      with TemporaryFile() as tmp:
        ttsScript = gTTS(script)
        ttsScript.write_to_fp(tmp)
        tmp.seek(0)
        source = discord.FFmpegPCMAudio(source=tmp, pipe=True)
        voice = await ctx.message.author.voice.channel.connect()
        voice.play(source)
        while(voice.is_playing()): None
        await voice.disconnect()
    except Exception as e:
      print(e)
      await Sounds.connectForSound(self, ctx.message.author, "NotNow.mp3")

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.meme.user:
      return
    if message.content.startswith(config['General']['Prefix']):
      soundsDict = await Sounds.getSoundDictionary()
      if message.content[1:] in soundsDict:
        await Sounds.connectForSound(self, message.author, soundsDict[message.content[1:]])

def setup(meme):
  meme.add_cog(Sounds(meme))