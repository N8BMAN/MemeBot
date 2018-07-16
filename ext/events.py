import discord, asyncio
from discord.ext import commands

class Events():
  def __init__(self, meme):
    self.meme = meme

  '''
  @meme.event
  async def on_voice_state_update(before, after):
    others = False
    for m in before.server.members:
      if m.id == "223222767384920081": #ryan
        member1 = m
      if m.id == "219195435783421954": #walk
        member2 = m
    #check if anyone else is on
    for c in member1.server.channels:
      if c.type == discord.ChannelType.voice:
        for m in c.voice_members:
          if m.id != member1.id and m.id != member2.id:
            others = True
    #if someone else is on do the thing
    if others:
      if member1.voice.voice_channel:
        if member2.voice.voice_channel:
          if len(member1.voice.voice_channel.voice_members) < 3 and member1.voice.voice_channel == member2.voice.voice_channel:
            for c in member1.server.channels:
              if  c.type == discord.ChannelType.voice:
                if c != member1.voice.voice_channel:
                  await meme.move_member(member1, c)
                  break
  '''	
  async def on_member_remove(self, member):
    for c in member.server.channels:
      if not c.permissions_for(member.server.me).send_messages:
        continue
      channel = c
      break
    invite = await self.meme.create_invite(destination = channel, xkcd = True, max_uses = 1)
    await self.meme.send_message(member, invite)
    
  async def on_member_ban(self, member):
    await self.meme.unban(member.server, member)

def setup(meme):
  meme.add_cog(Events(meme))