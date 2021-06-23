import discord
from discord.ext import commands

rolelist = {"fooRole": "855791882834280478"}
channelint = 855477991600422926
botintents = discord.Intents.default()
botintents.presences = True
botintents.members = True
botactivity = discord.Game(name="B$help")
botstatus = discord.Status.online
bot = commands.Bot(commands.when_mentioned_or('B$'),
                   activity=botactivity,
                   status=botstatus,
                   intents=botintents)
bot.remove_command("help")