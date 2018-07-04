import discord
from discord.ext import commands
import time
import asyncio

class Govern():
  def __init__(self, meme):
      self.meme = meme

  #member vars for voting purposes
  ballet = False
  voteCount = 0
  voterList = []
  allowImpeachment = True

  #returns list of members in a given role
  def members(self, ctx, role):
    roleMembers = []
    for m in ctx.message.author.server.members:
      if m.top_role == role:
        roleMembers.append(m)
    return roleMembers
  
  #returns second highest role (meme-bot is the true ruler)
  def getTopRole(self, ctx):
    numRoles = len(ctx.message.author.server.roles)
    for r in ctx.message.author.server.roles:
      if r.position == numRoles - 2:
        topRole = r
        break
    return r
  
  @commands.command(pass_context=True)
  async def impeach(self, ctx, nominee = None):
    """Impeach top admin, replace with @mention"""

    if self.ballet:
      await self.meme.say("There is already a vote going on!")
    
    elif not self.allowImpeachment:
      await self.meme.say("You must wait 24 hours between impeachments!")
    
    elif(not nominee):
      await self.meme.say("You must nominate a new president!")
    
    elif len(ctx.message.mentions) > 1:
      await self.meme.say("You can only nominate one person!")
    
    elif ctx.message.mentions[0] == ctx.message.author:
      await self.meme.say("You can't nominate yourself!")
    
    elif ctx.message.mentions[0].top_role == Govern.getTopRole(self, ctx):
      await self.meme.say(ctx.message.mentions[0].mention+" is already the president!")
    
    elif len(Govern.members(self, ctx, ctx.message.mentions[0].top_role)) > 1:
      await self.meme.say(ctx.message.mentions[0].mention+"'s role has more than one person!")
    
    else:
      nominee = ctx.message.mentions[0]
      current = Govern.members(self, ctx, Govern.getTopRole(self, ctx))[0]
      await self.meme.say("IMPEACHMENT TIME")
      await self.meme.say(nominee.mention + " vs " + current.mention)
      await self.meme.say("Type \"!vote\" to vote for impeachment.")
      await self.meme.say("5 votes needed!")
      self.ballet = True
      timer = time.time() + 300
      while time.time() < timer and self.voteCount < 5:
        await asyncio.sleep(1)
    
      await self.meme.say("Voting has ended!")
      if self.voteCount >= 5:
        await self.meme.say("The vote has passed! Swapping roles.")
        await self.meme.move_role(ctx.message.author.server, current.top_role, nominee.top_role.position)
        timer = time.time() + 5
        while time.time() < timer:
          await asyncio.sleep(1)
        await self.meme.move_role(ctx.message.author.server, nominee.top_role, len(ctx.message.author.server.roles)-2)
        self.allowImpeachment = False
        self.timer = time.time() + 86400
        self.voteCount = 0
        self.voterList = []
        self.ballet = False
        while time.time() < timer:
          await asyncio.sleep(1)
        self.allowImpeachment = True
      else:
        await self.meme.say(current.mention+" has not been impeached!")
        self.voteCount = 0
        self.voterList = []
        self.ballet = False
    
  @commands.command(pass_context=True)
  async def vote(self, ctx):
    """Vote for the current impeachment"""
    if not self.ballet:
      await self.meme.say("There is no vote going on")
    elif ctx.message.author in self.voterList:
      await self.meme.say("You already voted!")
    else:
      self.voterList.append(ctx.message.author)
      self.voteCount+=1
      await self.meme.say(str(5-self.voteCount)+" votes needed!")
    
  @commands.command(pass_context=True)
  async def list(self, ctx):
    """N8's Only."""
    for u in ctx.message.author.voice.voice_channel.voice_members:
      print(str(u.name))
    
  @commands.command(pass_context=True)
  async def moveTop(self, ctx, u=None):
    """N8's Only."""
    if u == None:
      await self.meme.say("You must mention someone")
    if ctx.message.author.id == "189495247762489344":
      u = ctx.message.mentions[0]
      await self.meme.move_role(ctx.message.author.server, u.top_role, len(ctx.message.author.server.roles)-2)
    else:
      await self.meme.say("No.")
    
  @commands.command(pass_context=True)
  async def swap(self, ctx, p1=None, p2=None):
    """N8's & Grffo's Only."""
    if ctx.message.author.id != "189495247762489344" and ctx.message.author.id != "140210955480072192":
      await self.meme.say("N8s and Grffos Only")
    elif p1 == None or p2 == None:
      await self.meme.say("You must mention 2 people")
    else:
      p1 = ctx.message.mentions[0]
      p2 = ctx.message.mentions[1]
      pos1 = p1.top_role.position
      await self.meme.move_role(ctx.message.author.server, p1.top_role, p2.top_role.position)
      timer = time.time() + 5
      while time.time() < timer:
        await asyncio.sleep(1)
      await self.meme.move_role(ctx.message.author.server, p2.top_role, pos1)
    
  @commands.command(pass_context=True)
  async def impeachCooldown(self, ctx):
    """N8's Only."""
    global allowImpeachment
    if ctx.message.author.id == "189495247762489344":
      allowImpeachment = False
      timer = time.time() + 43200
      while time.time() < timer:
        await asyncio.sleep(1)
      allowImpeachment = True
    self.meme.say("N8's Only.")

def setup(meme):
  meme.add_cog(Govern(meme))