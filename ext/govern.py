import discord
from discord.ext import commands
import time, random, re
import asyncio

class Govern(commands.Cog):
  def __init__(self, meme):
    self.meme = meme
    self.allowImpeachment = True
    self.active_vote = False
    self.voterList = []
    self.voteCount = 0
    self.challengers = []
  
  @commands.command()
  async def roll(self, ctx, *, rollCommand = None):
    """roll ndm->rolls m sided dice n times"""
    rollPattern = re.compile("[0-9]+d[0-9]+$")
    if(rollPattern.match(rollCommand)):
      roller = rollCommand.split("d")
      sum = 0
      if roller[0] == '0' or roller[1] == '0':
        await ctx.send("Rolling "+rollCommand+": "+str(sum))
        return
      if int(roller[0]) > 100:
        await ctx.send("First number can't be bigger than 100")
        return
      for x in range(0, int(roller[0])):
        sum += random.randint(1, int(roller[1]))
      await ctx.send(f"**Rolling {rollCommand}:** {sum}")
    else:
      await ctx.send("Roll should be in the form '(int)d(int)'")

  @commands.command()
  async def banDunky(self, ctx):
    """Bans Dunky, because everyone should be able to"""
    dunky = ctx.guild.get_member(226455807300993024)
    await ctx.guild.ban(dunky, reason="Memebot said so")
    await ctx.message.add_reaction('🇫')
    await asyncio.sleep(0.1)
    await ctx.message.add_reaction('🇦')
    await asyncio.sleep(0.1)
    await ctx.message.add_reaction('🇬')

  @commands.command()
  async def banSoy(self, ctx):
    """Bans Ryan, but only if you're dunky"""
    if(ctx.message.author.id == 226455807300993024):
      try:
        ryan = ctx.guild.get_member(223222767384920081)
        await ctx.guild.ban(ryan, reason="Memebot said so")
        await ctx.message.add_reaction('🇫')
        await asyncio.sleep(1)
        await ctx.message.add_reaction('🇦')
        await asyncio.sleep(1)
        await ctx.message.add_reaction('🇬')
      except Exception as e:
        await ctx.send("Ryan's not in this server.")
    else:
      await ctx.send("You're not Dunky")

  @commands.command()
  async def moveTop(self, ctx, member):
    """N8's Only"""
    if member == None:
      await ctx.send("You must mention someone")
    if ctx.message.author.id == 189495247762489344:
      member = ctx.message.mentions[0]
      await member.top_role.edit(position = len(ctx.guild.roles)-2)
    else:
      await ctx.send("No.")

  async def swapUtil(self, p1, p2):
    pos1 = p1.top_role.position
    await p1.top_role.edit(position=p2.top_role.position)
    await asyncio.sleep(5)
    await p2.top_role.edit(position=pos1)

  @commands.command()
  async def swap(self, ctx, p1=None, p2=None):
    """N8's & Grffo's Only."""
    if ctx.message.author.id != 189495247762489344 and ctx.message.author.id != 140210955480072192:
      await ctx.send("N8s and Grffos Only")
    elif p1 == None or p2 == None:
      await ctx.send("You must mention 2 people")
    else:
      p1 = ctx.message.mentions[0]
      p2 = ctx.message.mentions[1]
      await self.swapUtil(p1, p2)

  @commands.command()
  async def impeach(self, ctx, nominee = None):
    """Impeach top admin, replace with @mention"""
    if self.active_vote:
      await ctx.send("There is already a vote going on!")
    elif not self.allowImpeachment:
      await ctx.send("You must wait 24 hours between impeachments!")
    elif(not nominee):
      await ctx.send("You must nominate a new president!")
    elif len(ctx.message.mentions) > 1:
      await ctx.send("You can only nominate one person!")   
    elif ctx.message.mentions[0] == ctx.message.author:
      await ctx.send("You can't nominate yourself!")
    elif ctx.message.mentions[0].top_role == ctx.guild.roles[len(ctx.guild.roles)-2]:
      await ctx.send(ctx.message.mentions[0].mention+" is already the president!")
    elif len(ctx.message.mentions[0].top_role.members) > 1:
      await ctx.send(ctx.message.mentions[0].mention+"'s role has more than one person!")

    else:
      self.active_vote = True
      nominee = ctx.message.mentions[0]
      current = ctx.guild.roles[len(ctx.guild.roles)-2].members[0]
      await ctx.send("**IMPEACHMENT TIME**")
      await ctx.send(f"{nominee.mention} vs {current.mention}")
      await ctx.send("Type \"!vote\" to vote for impeachment.")
      await ctx.send("5 votes needed!")
      timer = time.time() + 300
      while time.time() < timer and self.voteCount < 5:
        await asyncio.sleep(1)

      await ctx.send("Voting has ended!")
      if self.voteCount >= 5:
        await ctx.send("The vote passed! Swapping roles.")
        await self.swapUtil(nominee, current)
      
        self.allowImpeachment = False
        self.voteCount = 0
        self.voterList = []
        self.active_vote = False
        await asyncio.sleep(86400)
        self.allowImpeachment = True
      else:
        await ctx.send(f"{current.mention} has not been impeached!")
        self.voteCount = 0
        self.voterList = []
        self.active_vote = False

  @commands.command()
  async def votekick(self, ctx, *, members=None):
    """Vote kick memer(s)"""
    if self.active_vote:
      await ctx.send("There is already a vote going on!")
    elif len(ctx.message.mentions) < 1:
      await ctx.send("You must mention at least one memer to kick!")
    else:
      self.active_vote = True
      await ctx.send("**VOTE KICK TIME**")
      if len(ctx.message.mentions) == 1:
        await ctx.send(f"Will we kick {ctx.message.mentions[0].mention}?")
      else:
        await ctx.send(f"Will we kick them all?")
      await ctx.send("Type \"!vote\" to vote yes.")
      await ctx.send("5 votes needed!")

      timer = time.time() + 300
      while time.time() < timer and self.voteCount < 5:
        await asyncio.sleep(1)

      await ctx.send("Voting has ended!")
      if self.voteCount >= 5:
        await ctx.send("The vote passed! They will be kicked.")
        for memer in ctx.message.mentions:
          await ctx.guild.ban(memer, reason="Memebot said so")
      else:
        await ctx.send("They will not be kicked!")
      self.voteCount = 0
      self.voterList = []
      self.active_vote = False

  async def attack(self, ctx, attacker, defender, hp_atk, hp_def):
    """Defines attacks for battles"""
    roll = random.randint(1, 20)
    if roll == 1:
      await ctx.send(f"Critical fail! {attacker.name} hurts themself for 10!\n")
      return hp_atk - 10, hp_def
    if roll == 20:
      await ctx.send(f"Critical hit! {attacker.name} hits {defender.name} for 40!\n")
      return hp_atk, hp_def - 40
    await ctx.send(f"{attacker.name} hits {defender.name} for {roll+10}\n")
    return hp_atk, hp_def - (10 + roll)

  async def battleMain(self, ctx, p1, p2):
    """Utility function for any battle commands"""
    await ctx.send(f"**BATTLE TIME**\n{p1.mention} vs. {p2.mention}")
    hp_p1, hp_p2, round_count = 100, 100, 0
    
    while(hp_p1 > 0 and hp_p2 > 0):
      await asyncio.sleep(2)
      if round_count % 2 == 0:
        hp_p1, hp_p2 = await self.attack(ctx, p1, p2, hp_p1, hp_p2)
      else:
        hp_p2, hp_p1 = await self.attack(ctx, p2, p1, hp_p2, hp_p1)
      if hp_p1 < 0: hp_p1 = 0
      if hp_p2 < 0: hp_p2 = 0
      await ctx.send(f"{p1.name}: {hp_p1} | {p2.name}: {hp_p2}")
      round_count += 1
    if hp_p1 == 0:
      await ctx.send(f"{p2.mention} defeated {p1.mention}!")
      return p2
    else:
      await ctx.send(f"{p1.mention} defeated {p2.mention}!")
      return p1
  
  @commands.command()
  async def battle(self, ctx, p1, p2=None):
    """Battle someone for memes"""
    if len(ctx.message.mentions) < 1:
      await ctx.send("You must mention someone to battle.")
    elif len(ctx.message.mentions) > 2:
      await ctx.send("Only two people can battle")
    elif len(ctx.message.mentions) == 1 and ctx.message.mentions[0] == ctx.message.author:
      await ctx.send("Kill yourself on your own.")
    elif len(ctx.message.mentions) == 2:
      await self.battleMain(ctx, ctx.message.mentions[0], ctx.message.mentions[1])
    else:
      await self.battleMain(ctx, ctx.message.mentions[0], ctx.message.author)

  @commands.command()
  async def challenge(self, ctx, target=None):
    """Challenge someone for their position"""
    if len(ctx.message.mentions) < 1:
      await ctx.send("You must mention someone to challenge")
    elif len(ctx.message.mentions) > 1:
      await ctx.send("You can only challenge one person")
    elif ctx.message.mentions[0].top_role.position < ctx.message.author.top_role.position:
      await ctx.send("You can only challenge people above you")
    elif ctx.message.mentions[0].top_role.position == len(ctx.guild.roles)-1:
      await ctx.send("You can't challenge GOD")
    elif ctx.message.author in self.challengers:
      await ctx.send("You must wait 24 hours between challenges")
    else:
      winner = await self.battleMain(ctx, ctx.message.mentions[0], ctx.message.author)
      if winner == ctx.message.author:
        await ctx.send("The challenger has succeeded! Swapping roles.")
        await self.swapUtil(ctx.message.mentions[0], ctx.message.author)
      else:
        await ctx.send("The challenger has failed! Penalizing challenger.")
        try:
          await ctx.message.author.top_role.edit(position=ctx.message.author.top_role.position-1)
        except:
          print("Whoops")
      self.challengers.append(ctx.message.author)
      await asyncio.sleep(86400)
      self.challengers.remove(ctx.message.author)
    

  @commands.command()
  async def vote(self, ctx):
    """Vote for the current ballet"""
    if not self.active_vote:
      await ctx.send("There is no vote going on")
    elif ctx.message.author in self.voterList:
      await ctx.send("You already voted!")
    else:
      self.voterList.append(ctx.message.author)
      self.voteCount+=1
      await ctx.send(str(5-self.voteCount)+" votes needed!")

def setup(meme):
  meme.add_cog(Govern(meme))