import configparser
from os.path import isfile

def init():
  global config
  config = configparser.ConfigParser()
  
  configName = 'memebot.ini'
  if not isfile(configName):
    createINI(configName)
  
  with open(configName, 'r') as configfile:
    config.read_file(configfile)
  

def createINI(configName):
  configNew = configparser.ConfigParser()
  configNew['General'] = {}
  configNew['General']['Token'] = input("Config file not found! Enter your bot token: ")
  configNew['General']['CogsDir'] = 'ext'
  configNew['General']['Prefix'] = '!'
  configNew['Plex'] = {}
  configNew['Plex']['RadarrToken'] = 'Enter token'
  configNew['Plex']['RadarrURL'] = 'Enter urlbase'
  configNew['Plex']['PlexToken'] = 'Enter token'
  configNew['Plex']['PlexURL'] = 'Enter urlbase'
  with open(configName, 'w') as configfile:
    configNew.write(configfile)
  print("Config file created!\n")