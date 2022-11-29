import discord
from discord.ext import commands


rolelist = {"fooRole": "855791882834280478"}
# channelint = 855498805516566538
channelint = 1047109252973596724 # botz
botintents = discord.Intents.all()
botintents.presences = True
botintents.members = True
botactivity = discord.Game(name="B$help")
# botstatus = discord.Status.online
botstatus = discord.Status.dnd
bot = commands.Bot(commands.when_mentioned_or('B$'),
                   activity=botactivity,
                   status=botstatus,
                   intents=botintents)
bot.remove_command("help")

igUsernames = ['binus_bandung','fypbinus','sadc.binusbandung','informatics.binusbandung','himtibinusbandung']

lomba_rolelist = {
    "cp": "Competitive Programming",
    "ctf":"CTF, CyberSec, InfoSec"}