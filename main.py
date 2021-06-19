from emoji import UNICODE_EMOJI
import sys
from replit import db
from keep_alive import keep_alive
import discord
import os
import requests
import random
import json
import datetime
from discord.ext import commands

# Copas dari readme
# * FEATURE READY:
# Keyword nya B$ gatau ntar ganti ato gimana
# ini masih ngasal sih, nanti di delete kayanya
# inspire : sends a random quote
# encouragement word (kena keyword tertentu bakal nge cheer up) (CRUD ready)

# TODO:
# Migrate on message commands to bot commands

# Features - TOADD:

# -. B$help
#   Send keyword + info bot

# 1. Info Binus
#   Cari/Bikin API instagram post grabber
#   Pake keywoard buat nyaring info tertentu

# 2. Reminder Deadline Tugas
#   Format:
#   B$reminder [nama_tugas] [dd/mm/yyyy] [HH:MM] [tag_siapa_aja?]
#   Contoh:
#   B$reminder PRLinearAlgebraWeek1 02/02/2022 23:00 everyone
#   .
#   ribet di tag kayanya, ntar bikin role per kelas juga (kelas kita kebagi 2/3 kayanya)

# 3. Reminder Jadwal Kuliah
#   tfw blom dapet jadwal kuliah
#   nanti bikin API get jadwal kuliah
#   ^kalo mager input jadwal kuliah sendiri ke DB nya

activity = discord.Game(
    name=
    "Bot nya lagi dibikin.\nIde:\nReminder Tugas,\nInfo Binus,\nReminder Jadwal Kelas"
)

bot = commands.Bot(command_prefix="B$",
                   activity=activity,
                   status=discord.Status.dnd)

sadwords = ["bruh", "sad", "qq", "😞", "fuck", "ajg"]

blankobj = {}

starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person / bot!"
]


# FUNCTIONS
def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    db["encouragements"] = encouragements


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

@bot.command(name ="resetreminder")
async def initdbbf(ctx):
      del db["reminder"]
      await ctx.channel.send("reset done")

#   B$reminder [nama_tugas] [dd/mm/yyyy] [HH:MM] [tag_siapa_aja?]
@bot.command(name ="reminder")
async def reminderbf(ctx,namatugas,datestr,timestr,tag):
    dateint = datetime.datetime.strptime(datestr, "%d/%m/%Y")
    timeint = datetime.datetime.strptime(timestr, "%H:%M")
    dateobj = dateint + datetime.timedelta(hours = timeint.hour, minutes = timeint.minute)
    dateobjtostr = datetime.datetime.strftime(dateobj, "%d/%m/%Y %H/%M")
    remindobj = [
      dateobjtostr,
      namatugas,
      tag
    ]
    if "reminder" in db.keys():
      dbr = db["reminder"]
      dbr.append(remindobj)
    else:
      db["reminder"] = remindobj
    await ctx.channel.send("Reminder {} set to {} {} for {}".format(namatugas,datestr,timestr,tag))
# Jadi di database reminder teh isinya list remindobj itu.
# Rada penting: si tanggalnya string, kalo dalam bentuk date object gabisa masuk ke db

@bot.command(name ="listreminder")
async def listreminderbf(ctx):
    if "reminder" in db.keys():
      await ctx.channel.send(db["reminder"])
    else:
      await ctx.channel.send("There's no reminder at the moment!")
      await ctx.channel.send("Try adding one with this format:")
      await ctx.channel.send("B$reminder nama_tugas 31/03/2022 23:59 me")

# ----

# ON READY
@bot.event
async def on_ready():
    print(db["reminder"])
    print('We have logged in as {0.user}'.format(bot))
    # Channel ID goes here
    await bot.get_channel(855477991600422926).send(
        "Hi I'm ready, B$help to get commands")


# ON MESSAGE
@bot.event
async def on_message(message):
    # AVOIDS SELF COMMAND
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    msg = message.content

    if msg.startswith('B$hello'):
        await message.channel.send('Hello!')

    # init Encouragement Words from Array and DB
    options = starter_encouragements
    if "encouragements" in db.keys():
        options.extend(db["encouragements"])

    # Find sad words
    if any(word in msg for word in sadwords):
        await message.channel.send(random.choice(options))


    # ! Migrate to bot command
    if msg.startswith("B$new"):
        encouraging_message = msg.split("B$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("B$del"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split("B$del ", 1)[1])
            delete_encouragement(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)
        await message.channel.send("Changes will be made on restart 😞")
        await message.channel.send("Type B$restart to restart me.")


my_secret = os.environ['TOKEN']

keep_alive()  # AUTO PING
bot.run(my_secret)
