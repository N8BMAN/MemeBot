import discord, asyncio
from discord.ext import commands

class Events():
  def __init__(self, meme):
    self.meme = meme
    self.recentBans = []

  async def on_member_remove(self, member):
    try:
      invite = await member.guild.system_channel.create_invite(max_uses=1)
      if not member.dm_channel:
        await member.create_dm()
      channel = member.dm_channel
      await channel.send(invite)
      self.recentBans.append(member)
    except Exception as e:
      print(f"Couldn't send invite to {member.name}: {e}")
    
  async def on_member_ban(self, guild, member):
    await guild.unban(member)

  async def on_member_join(self, member):
    if member in self.recentBans:
      await member.add_roles(self.recentBans[self.recentBans.index(member)].top_role)
      self.recentBans.remove(member)
def setup(meme):
  meme.add_cog(Events(meme))