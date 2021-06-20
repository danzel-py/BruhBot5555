from emoji import UNICODE_EMOJI
import cog
import sys
from replit import db
import abc
from keep_alive import keep_alive
import discord
from discord.utils import get
import os
import requests
import math
import random
import time
import json
import datetime
from discord.ext import commands,tasks

# CSB25 - 855440129434714112
# ucb - 855477991600422926
channelint = 855477991600422926

#manual :v
rolelist = ["everyone"]

activity = discord.Game(
    name=
    "Bot nya lagi dibikin.\nIde:\nReminder Tugas,\nInfo Binus,\nReminder Jadwal Kelas"
)

botstatus = discord.Status.online

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(commands.when_mentioned_or('B$'),
                   activity=activity,
                   status=botstatus,
                   help_command = help_command)


# FUNCTIONS
def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

def todaysQuote():
    response = requests.get("https://zenquotes.io/api/today")
    json_data = json.loads(response.text)
    quote = "Good Morning! Here's a quote to start the day.\n\n> *"+json_data[0]['q']+"*" + " \n\n-" + json_data[0]['a']
    return (quote)



def dateToStr(datestr,timestr): # accepts d/m/Y and H:M
    # Fungsi ini buat timezone WIB GMT+7!
    dateint = datetime.datetime.strptime(datestr, "%d/%m/%Y")
    timeint = datetime.datetime.strptime(timestr, "%H:%M")
    dateobj = dateint + datetime.timedelta(hours = timeint.hour - 7, minutes = timeint.minute)
    dateobjtostr = datetime.datetime.strftime(dateobj, "%d/%m/%Y %H:%M")
    return dateobjtostr

def strToDate(strdate):
  dateobj = datetime.datetime.strptime(strdate, "%d/%m/%Y %H:%M")
  return dateobj
  




def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


# ----

# Reminder
class Reminder(commands.Cog):
  #   B$reminder [nama_tugas] [dd/mm/yyyy] [HH:MM] [tag_siapa_aja?]

# * ADD REMINDER

# everyone: 855701462793453578
  def __init__(self, bot):
        self.bot = bot

  @commands.command(name ="reminder", brief = "`B$help reminder`")
  async def reminderbf(self,ctx,namatugas,tanggal,jam,tag):
      finalstr = dateToStr(tanggal,jam)
      if(tag == "me"):
        tag = "<@{}>".format(str(ctx.message.author.id))
      remindobj = [
        finalstr,
        namatugas,
        tag
      ]
      if "reminder" in db.keys():
        dbr = db["reminder"]
        dbr.append(remindobj)
      else:
        db["reminder"] = [remindobj]
      await ctx.channel.send("Reminder {} set to {} {} for {}".format(namatugas,tanggal,jam,tag))

  #
  # Jadi di database reminder teh isinya list remindobj itu.
  # Rada penting: si tanggalnya string, kalo dalam bentuk date object gabisa masuk ke db

  # TODO: UNDO ADD REMINDER



  @commands.command(name ="listreminder",brief ="show upcoming events")
  async def listreminderbf(self,ctx):
      now = datetime.datetime.now() + datetime.timedelta(hours = 9, minutes = 5)
      if "reminder" in db.keys():
        if db["reminder"]:
        # await ctx.channel.send(db["reminder"])
          await ctx.channel.send("Upcoming events:")
          for rm in db["reminder"]:
            await ctx.channel.send('-')
            await ctx.channel.send("{} - {}".format(rm[1],rm[2]))
            await ctx.channel.send(datetime.datetime.strftime(
              datetime.datetime.strptime(rm[0], "%d/%m/%Y %H:%M") + datetime.timedelta(hours = 7),
              "%d/%m/%Y %H:%M"
            ))
            diff = datetime.datetime.strptime(rm[0], "%d/%m/%Y %H:%M")-datetime.datetime.now()
            difd = diff.days
            difs = diff.seconds
            difh = math.floor(difs/3600)
            difm = math.floor((difs%3600)/60)
            if difd>25:
              await ctx.channel.send("Due in more than 25 days 💤")
            else:
              difhh = difd*24 + difh
              await ctx.channel.send("⚠️ Due in {} hour(s) and {} minute(s) ⚠".format(difhh,difm))
        else:
          await ctx.channel.send("There's no reminder at the moment!")
          await ctx.channel.send("Try adding one with this format: (in GMT+7/WIB please)")
          await ctx.channel.send("B$reminder nama_tugas {} me".format(datetime.datetime.strftime(now,"%d/%m/%Y %H:%M")))

      else:
        await ctx.channel.send("There's no reminder at the moment!")
        await ctx.channel.send("Try adding one with this format: (in GMT+7/WIB please)")
        await ctx.channel.send("B$reminder nama_tugas {} me".format(datetime.datetime.strftime(now,"%d/%m/%Y %H:%M")))



# COMMANDS
@bot.command(name="restart",brief="restart bot")
async def restartbf(ctx):
    await ctx.channel.send("Please wait...")
    restart_bot()

@bot.command(name ="inspire", brief = "inspiration +99")
async def inspirebf(ctx):
    await ctx.channel.send(getQuote())

bot.add_cog(Reminder(bot))

# ----

# ON READY
@bot.event
async def on_ready():
    if "reminder" in db.keys():
      print(db["reminder"])
    remindFunction.start()
    dailyQuotes.start()
    print('We have logged in as {0.user}'.format(bot))
    # Channel ID goes here
    await bot.get_channel(channelint).send(
        "Hi I'm ready, `B$help` to get commands.")


# ON MESSAGE blm kepake
@bot.event
async def on_message(message):
    # AVOIDS SELF COMMAND
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    msg = message.content

    if msg.startswith("adm00nify"):
      autt = message.author
      await autt.add_roles(855678482516672543)
      await message.channel.send(autt.id)

    if msg.startswith(('thanks bot','Thanks bot','Thanks Bot')):
      await message.channel.send('Your Welcome, 御主人様!')

    if msg.startswith('B$hello'):
        await message.channel.send('Hello!')

    # Reset Reminder
    if msg.startswith('B$resetreminder'):
        channel = message.channel
        await channel.send('u sure mate? yes/no')

        def check(m):
            return m.content == 'yes' and m.channel == channel

        henji = await bot.wait_for('message', check=check)
        if "reminder" in db.keys():
          del db["reminder"]
        else:
          channel.send("bruh issalready empty")
        await channel.send('Deleted bruh.'.format(henji))



# b25 everyone: 855701462793453578
# ucb everyone: 855703085825785856
@tasks.loop(minutes=1)
async def remindFunction():
    print('letscheck')
    now = datetime.datetime.now()
    if "reminder" in db.keys():
      for rm in db["reminder"]:
        roleexist = -1
        print(rm[0])
        print(datetime.datetime.strftime(now,"%d/%m/%Y %H:%M"))
        stringrm = rm[0]
        daterm = strToDate(stringrm)
        datermhminus1 = daterm + datetime.timedelta(hours = -1)
        datermmminus10 = daterm + datetime.timedelta(minutes = -10)
        strhminus1 = datetime.datetime.strftime(datermhminus1,"%d/%m/%Y %H:%M")
        strmminus10 = datetime.datetime.strftime(datermmminus10,"%d/%m/%Y %H:%M")

        if strmminus10 == now.strftime("%d/%m/%Y %H:%M"):
          if rm[2] in rolelist:
            roleexist = 1

          if roleexist != -1:
            await bot.get_channel(channelint).send("tag: @{} ".format(rm[2]))
          await bot.get_channel(channelint).send("🚨 Hey {} it's 10 minutes to {}. Gotta go fast!".format(rm[2],rm[1]))
        if strhminus1 == now.strftime("%d/%m/%Y %H:%M"):
          if rm[2] in rolelist:
            roleexist = 1

          if roleexist != -1:
            await bot.get_channel(channelint).send("tag: @{} ".format(rm[2]))
          await bot.get_channel(channelint).send("Hey {} it's 1 hour to {}.".format(rm[2],rm[1]))
        if rm[0] == now.strftime("%d/%m/%Y %H:%M"):
          # ?Question: How do i get list of all roles?
          # unsolved
          # TODO: masukin roles manual :v
          if rm[2] in rolelist:
            roleexist = 1

          if roleexist != -1:
            await bot.get_channel(channelint).send("tag: @{} ".format(rm[2]))
          await bot.get_channel(channelint).send("Hey {} it's time to {}.".format(rm[2],rm[1]))

        elif strToDate(rm[0]) < now :
          db["reminder"].remove(rm)
          print("dah lewat")
    else:
      return

@tasks.loop(hours = 1)
async def dailyQuotes():
  print('getting quotes...')
  now = datetime.datetime.now()
  sixaclock = now.replace(hour = 22, minute = 0, second = 0, microsecond = 0)
  sevenaclock = now.replace(hour = 23, minute = 0, second = 0, microsecond = 0)
  if(now < sevenaclock and now > sixaclock):
    await bot.get_channel(channelint).send(todaysQuote())



my_secret = os.environ['TOKEN']



keep_alive()  # AUTO PING
bot.run(my_secret)
