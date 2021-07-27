import discord
from discord.ext import commands

# bot commands b25bdg 855498805516566538
# testing channel 855477991600422926

rolelist = {"fooRole": "855791882834280478"}
channelint = 855498805516566538
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

igUsernames = ['binus_bandung','fypbinus','sadc.binusbandung','informatics.binusbandung','himtibinusbandung']