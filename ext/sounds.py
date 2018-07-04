import discord
from discord.ext import commands

class Sounds():
  def __init__(self, meme):
    self.meme = meme

  #function to connect to voice channel, and start playing -- all commands call this
  async def connectForSound(self, member, file):
    if(member.voice.voice_channel):
      voice = await self.meme.join_voice_channel(member.voice.voice_channel)
      player = voice.create_ffmpeg_player('ext/clip/'+file)
      player.start()
      while(player.is_playing()):
        None
      await voice.disconnect()

  @commands.command(pass_context=True)
  async def nou(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'NoU.m4a')
    
  @commands.command(pass_context=True)
  async def steamed(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'steamed-hams.mp3')

  @commands.command(pass_context=True)
  async def number15(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'footlettuce.mp3')
    
  @commands.command(pass_context=True)
  async def orbs(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'ORBS.mp3')
    
  @commands.command(pass_context=True)
  async def quack(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'quack.mp3')
      
  @commands.command(pass_context=True)
  async def bazinga(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'bazinga.mp3')
    
  @commands.command(pass_context=True)
  async def ree(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'ree.mp3')
    
  @commands.command(pass_context=True)
  async def cartman(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'cartman.mp3')

  @commands.command(pass_context=True)
  async def skidaddle(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'skidaddle.mp3')
    
  @commands.command(pass_context=True)
  async def birdup(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'birdup.mp3')
    
  @commands.command(pass_context=True)
  async def pussy(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'pussy.mp3')

  @commands.command(pass_context=True)
  async def eddy(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'ed_murph.mp3')
  
  @commands.command(pass_context=True)
  async def revolution(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'ussr.mp3')
  
  @commands.command(pass_context=True)
  async def smoke(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'smoke.mp3')

  @commands.command(pass_context=True)
  async def luigi(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'luigi.wav')

  '''
  @commands.command(pass_context=True)
  async def flute(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'flute.mp3')
  '''
  
  @commands.command(pass_context=True)
  async def hmm(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'hmm.mp3')
  
  @commands.command(pass_context=True)
  async def aeiou(self, ctx):
    """~~~~SOUNDS BEGIN~~~~"""
    await Sounds.connectForSound(self, ctx.message.author, 'aarug.mp3')
  
  @commands.command(pass_context=True)
  async def hai(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'mark.mp3')
  
  @commands.command(pass_context=True)
  async def destroy(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'destroy.wav')
  
  @commands.command(pass_context=True)
  async def scanning(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'alex.mp3')
  
  @commands.command(pass_context=True)
  async def areyousure(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'areyou.mp3')
  
  @commands.command(pass_context=True)
  async def birth(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'birth.mp3')
  
  @commands.command(pass_context=True)
  async def argonian(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'argonian.mp3')
  
  @commands.command(pass_context=True)
  async def call(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'call.mp3')
  
  @commands.command(pass_context=True)
  async def xanny(self, ctx):
    """~~~~SOUNDS END~~~~"""
    await Sounds.connectForSound(self, ctx.message.author, 'xanny.mp3')
  
  @commands.command(pass_context=True)
  async def hat(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'hat.mp3')
  
  @commands.command(pass_context=True)
  async def box(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'box.mp3')

  @commands.command(pass_context=True)
  async def order66(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'order66.mp3')
  
  @commands.command(pass_context=True)
  async def gtfo(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'gtfo.mp3')
  
  @commands.command(pass_context=True)
  async def right(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'right.mp3')
  
  @commands.command(pass_context=True)
  async def left(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'left.mp3')
  
  @commands.command(pass_context=True)
  async def brum(self, ctx):
    await Sounds.connectForSound(self, ctx.message.author, 'brum.m4a')


def setup(meme):
  meme.add_cog(Sounds(meme))