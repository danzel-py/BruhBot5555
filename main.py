from emoji import UNICODE_EMOJI
import sys
from replit import db
from keep_alive import keep_alive
import discord
import os
import requests
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

bot = commands.Bot(command_prefix="B$",
                   activity=activity,
                   status=discord.Status.dnd)


# FUNCTIONS
def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
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


# COMMANDS
@bot.command(name="restart")
async def restartbf(ctx):
    await ctx.channel.send("Please wait...")
    restart_bot()
@bot.command(name ="inspire")
async def inspirebf(ctx):
    await ctx.channel.send(getQuote())


#   B$reminder [nama_tugas] [dd/mm/yyyy] [HH:MM] [tag_siapa_aja?]

# * ADD REMINDER

# everyone: 855701462793453578

@bot.command(name ="reminder")
async def reminderbf(ctx,namatugas,datestr,timestr,tag):
    finalstr = dateToStr(datestr,timestr)
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
    await ctx.channel.send("Reminder {} set to {} {} for {}".format(namatugas,datestr,timestr,tag))

#
# Jadi di database reminder teh isinya list remindobj itu.
# Rada penting: si tanggalnya string, kalo dalam bentuk date object gabisa masuk ke db

# TODO: UNDO ADD REMINDER



@bot.command(name ="listreminder")
async def listreminderbf(ctx):
    if "reminder" in db.keys():
      # await ctx.channel.send(db["reminder"])
      await ctx.channel.send("Upcoming events:")
      for rm in db["reminder"]:
        await ctx.channel.send('-')
        await ctx.channel.send("{} - {}".format(rm[1],rm[2]))
        await ctx.channel.send(rm[0])
    else:
      await ctx.channel.send("There's no reminder at the moment!")
      await ctx.channel.send("Try adding one with this format: (in GMT+7/WIB please)")
      await ctx.channel.send("B$reminder nama_tugas 31/03/2022 23:59 me")

# ----

# ON READY
@bot.event
async def on_ready():
    if "reminder" in db.keys():
      print(db["reminder"])
    remindFunction.start()
    print('We have logged in as {0.user}'.format(bot))
    # Channel ID goes here
    await bot.get_channel(channelint).send(
        "Hi I'm ready, B$help to get commands.")


# ON MESSAGE blm kepake
@bot.event
async def on_message(message):
    # AVOIDS SELF COMMAND
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    msg = message.content

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
          await bot.get_channel(channelint).send("(THIS IS AN AUTOMATED MESSAGE)")
          if rm[2] in rolelist:
            roleexist = 1

          if roleexist != -1:
            await bot.get_channel(channelint).send("tag: @{} ".format(rm[2]))
          await bot.get_channel(channelint).send("Hey {} it's 10 minutes to {}".format(rm[2],rm[1]))
        if strhminus1 == now.strftime("%d/%m/%Y %H:%M"):
          await bot.get_channel(channelint).send("(THIS IS AN AUTOMATED MESSAGE)")
          if rm[2] in rolelist:
            roleexist = 1

          if roleexist != -1:
            await bot.get_channel(channelint).send("tag: @{} ".format(rm[2]))
          await bot.get_channel(channelint).send("Hey {} it's 1 hour to {}".format(rm[2],rm[1]))
        if rm[0] == now.strftime("%d/%m/%Y %H:%M"):
          await bot.get_channel(channelint).send("(THIS IS AN AUTOMATED MESSAGE)")
          # ?Question: How do i get list of all roles?
          # unsolved
          # TODO: masukin roles manual :v
          if rm[2] in rolelist:
            roleexist = 1

          if roleexist != -1:
            await bot.get_channel(channelint).send("tag: @{} ".format(rm[2]))
          await bot.get_channel(channelint).send("Hey {} it's time to {}".format(rm[2],rm[1]))

        elif strToDate(rm[0]) < now :
          db["reminder"].remove(rm)
          print("dah lewat")
    else:
      return


my_secret = os.environ['TOKEN']


keep_alive()  # AUTO PING
bot.run(my_secret)
