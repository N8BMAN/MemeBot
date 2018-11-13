import discord, asyncio
from discord.ext import commands
import time, json, requests, configparser
from plexapi.server import PlexServer
import settings

class Plex():
  def __init__(self, meme):
    self.meme = meme

    self.userCooldown = []
    self.api_token = settings.config['Plex']['RadarrToken']
    self.api_url_base = settings.config['Plex']['RadarrURL']
    self.plex_token = settings.config['Plex']['PlexToken']
    self.plex_baseurl = settings.config['Plex']['PlexURL']

    self.plex = PlexServer(self.plex_baseurl, self.plex_token)


  async def get_movie_search(self, searchTerm):
    api_url = "{0}{1}".format(self.api_url_base, '/movie/lookup')
    req = {'term' : searchTerm, 'apikey' : self.api_token}
  
    response = requests.get(api_url, params=req)
  
    if response.status_code == 200:
      return json.loads(response.content.decode('utf-8'))
    else:
      return None
    

  async def add_movie(self, ctx, movie):
    api_url = "{0}{1}".format(self.api_url_base, '/movie')
    headers = {'X-Api-Key': self.api_token}
    response = requests.post(api_url, json=movie, headers=headers)
  
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
      await ctx.send("Movie added sucessfully!")
    else:
      await ctx.send("Movie failed to be added...")

    await asyncio.sleep(5)
    api_url = "{0}{1}".format(self.api_url_base, '/command')
    response = requests.post(api_url, json={'name': "missingMoviesSearch", 'filterKey': "status", 'filterValue': "released"}, headers=headers)


  @commands.command(pass_context = True)
  async def addMovie(self, ctx, *, searchTerm = None):
    """Add Movies to plex. !addMovie 'movie name'"""
    if ctx.message.author in self.userCooldown:
      await ctx.send("You must wait 24 hours in between requests!")
    elif searchTerm == None:
      await ctx.send("You must enter a search term!")
    else:
      try:
        search = await Plex.get_movie_search(self, searchTerm)
        searchClone = search[:]
        plex_movies = self.plex.library.section('Movies')
        for movie in search:
          plex_search = plex_movies.search(title = movie['title'], year = movie['year'])
          if len(plex_search) > 0 or movie['status'] != 'released':
            searchClone.remove(movie)

        search = searchClone[:]
        x = 0
        searchResults = ''

        embed = discord.Embed(title="", description="", color=0x00ff00)
        for movie in search:
          x+=1
          searchResults += (str(x)+": "+movie['title']+" ("+str(movie['year'])+")\n")
        embed.add_field(name = "Search Results", value = searchResults, inline=False)
        embed.set_footer(text = '*note, movies already on Plex, and movies not on bluray yet are not listed')
        await ctx.send(embed = embed)

        selection = ''
        def check(m):
          return m.author == ctx.message.author
        while(not str(selection).isdigit() or int(selection) < 1 or int(selection) > x):
          await ctx.send('Select a movie to add, 1 to '+str(x)+'. or type \'cancel\'')
          msg = await self.meme.wait_for('message', check = check, timeout = 30)
          if msg == None or msg.content == 'cancel':
            await ctx.send('Search cancelled.')
            return  
          selection = msg.content

        if not selection == None:
          movie = search[int(selection)-1]
          movie['qualityProfileId'] = 4
          movie['rootFolderPath'] = 'E:\Videos\Movies'
          movie['monitored'] = True
          await Plex.add_movie(self, ctx, movie)
          self.userCooldown.append(ctx.message.author)
          await asyncio.sleep(86400)
          self.userCooldown.remove(ctx.message.author)
      except Exception as e:
        await ctx.send(f"Something broke. Try a different search term. {e}")


def setup(meme):
  meme.add_cog(Plex(meme))