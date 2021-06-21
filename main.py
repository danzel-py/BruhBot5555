from emoji import UNICODE_EMOJI
import sys
from replit import db
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
import re
import asyncio
from discord.ext import commands, tasks

# BUG tagged as #broken

channelint = 855477991600422926

intents = discord.Intents.default()
intents.presences = True
intents.members = True

activity = discord.Game(name="B$help")

botstatus = discord.Status.online

help_command = commands.DefaultHelpCommand(no_category='Commands')

bot = commands.Bot(commands.when_mentioned_or('B$'),
                   activity=activity,
                   status=botstatus,
                   intents=intents)

bot.remove_command("help")

#manual :v
rolelist = {"fooRole": "855791882834280478"}


# FUNCTIONS
def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def todaysQuote():
    response = requests.get("https://zenquotes.io/api/today")
    json_data = json.loads(response.text)
    quote = "Good Morning! Here's a quote to start the day.\n\n> *" + json_data[
        0]['q'] + "*" + " \n\n-" + json_data[0]['a']
    return (quote)


#embed=discord.Embed(title="We have {} reminder(s) today")
# embed.set_author(name="TODAYS REMINDER")
# embed.add_field(name="name", value="val", inline=False)
# await ctx.send(embed=embed)


def dailyReminder(htoplus):
    if htoplus == 7:
        tpll = "today"
        tplx = "Today"
    elif htoplus == 7+24:
        tpll = "tomorrow"
        tplx = "Tomorrow"
    now = datetime.datetime.now()
    instr = datetime.datetime.strftime(now + datetime.timedelta(hours=htoplus),
                                       "%d/%m/%Y")
    if "reminder" in db.keys():
        ct = 0
        if db["reminder"]:
            for rm in db["reminder"]:
                rmobj = datetime.datetime.strptime(rm[0], "%d/%m/%Y %H:%M")
                therm = datetime.datetime.strftime(
                    rmobj + datetime.timedelta(hours=7), "%d/%m/%Y")
                if therm == instr:
                    ct += 1
            embed = discord.Embed(
                title="{}'s reminder".format(tplx),
                description="We have {} reminder(s) {}".format(ct,tpll),
                color=0x43b8ea)
            for rm in db["reminder"]:
                rmobj = datetime.datetime.strptime(rm[0], "%d/%m/%Y %H:%M")
                therm = datetime.datetime.strftime(
                    rmobj + datetime.timedelta(hours=7), "%d/%m/%Y")
                if therm == instr:
                    yourname = rm[2]
                    if yourname == "@everyone":
                        yourname = "everyone"
                    if yourname[0] == '<':
                        x = re.split("\@|\>", yourname)
                        if (x[1][0] == '&'):
                            for ky in rolelist:
                                if rolelist[ky] == x[1][1:]:
                                    yourname = ky
                        else:
                            yourname = rm[3]
                    embed.add_field(name="{} - {}".format(rm[1], yourname),
                                    value=stringUtcToGmt(rm[0])[11:],
                                    inline=False)
        else:
            embed = discord.Embed(title="{}'s REMINDER".format(tplx),
                                  description="No upcoming events for {}".format(tpll))
    else:
        embed = discord.Embed(title="{}'s REMINDER".format(tplx),
                              description="No upcoming events for {}".format(tpll))
    return embed


def stringDateCombine(datestr, timestr):  # accepts d/m/Y and H:M
    # Fungsi ini buat timezone WIB GMT+7 ke UTC
    dateint = datetime.datetime.strptime(datestr, "%d/%m/%Y")
    timeint = datetime.datetime.strptime(timestr, "%H:%M")
    dateobj = dateint + datetime.timedelta(hours=timeint.hour - 7,
                                           minutes=timeint.minute)
    dateobjtostr = datetime.datetime.strftime(dateobj, "%d/%m/%Y %H:%M")
    return dateobjtostr


def stringUtcToGmt(utcstr):
    gmtdate = datetime.datetime.strptime(
        utcstr, "%d/%m/%Y %H:%M") + datetime.timedelta(hours=7)
    gmtstr = datetime.datetime.strftime(gmtdate, "%d/%m/%Y %H:%M")
    return gmtstr


def strToDate(strdate):
    dateobj = datetime.datetime.strptime(strdate, "%d/%m/%Y %H:%M")
    return dateobj


def jamFilter(jam):
    if jam == "midnight": return "23:59"
    if jam == "midnoon": return "12:00"
    jam = re.sub('\.', ':', jam)
    pospostam = re.search("\d+:\d+am", jam)
    pospostpm = re.search("\d+:\d+pm", jam)
    posam = re.search("am", jam)
    pospm = re.search("pm", jam)
    if pospostam:
        jam = jam[0:posam.start()]
        return jam
    if pospostpm:
        jam = jam[0:pospm.start()]
        poscolon = re.search(":", jam)
        jamdepan = jam[0:poscolon.start()]
        jambelakang = jam[poscolon.start():]
        jam = str(int(jamdepan) + 12) + jambelakang
        return jam
    if posam:
        jam = jam[0:posam.start()] + ":00"
        return jam
    if pospm:
        jam = jam[0:pospm.start()]
        jam = str(int(jam) + 12) + ":00"
        return jam
    truthyclock = re.search("\d+:\d+", jam)
    if truthyclock:
        return jam
    else:
        return "ERR"


def tanggalFilter(tanggal):
    now = datetime.datetime.now()
    tmrw = now + datetime.timedelta(days=1)
    tmrw2 = now + datetime.timedelta(days=2)
    nxtwk = now + datetime.timedelta(weeks=1)

    def nextdayinweek(intday, week):
        dateobj = now + datetime.timedelta(days=-now.weekday() + intday,
                                           weeks=week)
        return datetime.datetime.strftime(dateobj, "%d/%m/%Y")

    if (tanggal == "today" or tanggal == "hariini"):
        tanggal = datetime.datetime.strftime(now, "%d/%m/%Y")
    elif (tanggal == "tomorrow" or tanggal == "besok"):
        tanggal = datetime.datetime.strftime(tmrw, "%d/%m/%Y")
    elif (tanggal == "dayaftertomorrow" or tanggal == "lusa"):
        tanggal = datetime.datetime.strftime(tmrw2, "%d/%m/%Y")
    elif (tanggal == "mingdep" or tanggal == "nextweek"):
        tanggal = datetime.datetime.strftime(nxtwk, "%d/%m/%Y")
    elif (tanggal == "nextmonday" or tanggal == "nextmon"
          or tanggal == "senindepan"):
        tanggal = nextdayinweek(0, 1)
    elif (tanggal == "nexttuesday" or tanggal == "nexttue"
          or tanggal == "selasadepan"):
        tanggal = nextdayinweek(1, 1)
    elif (tanggal == "nextwednesday" or tanggal == "nextwed"
          or tanggal == "rabudepan"):
        tanggal = nextdayinweek(2, 1)
    elif (tanggal == "nextthursday" or tanggal == "nextthu"
          or tanggal == "kamisdepan"):
        tanggal = nextdayinweek(3, 1)
    elif (tanggal == "nextfriday" or tanggal == "nextfri"
          or tanggal == "jumatdepan"):
        tanggal = nextdayinweek(4, 1)
    elif (tanggal == "nextsaturday" or tanggal == "nextsat"
          or tanggal == "sabtudepan"):
        tanggal = nextdayinweek(5, 1)
    elif (tanggal == "nextsunday" or tanggal == "nextsun" or tanggal == "sun"
          or tanggal == "minggu"):
        tanggal = nextdayinweek(6, 1)
    elif (tanggal == "monday" or tanggal == "mon" or tanggal == "senin"):
        tanggal = nextdayinweek(0, 0)
    elif (tanggal == "tuesday" or tanggal == "tue" or tanggal == "selasa"):
        tanggal = nextdayinweek(1, 0)
    elif (tanggal == "wednesday" or tanggal == "wed" or tanggal == "rabu"):
        tanggal = nextdayinweek(2, 0)
    elif (tanggal == "thursday" or tanggal == "thu" or tanggal == "kamis"):
        tanggal = nextdayinweek(3, 0)
    elif (tanggal == "friday" or tanggal == "fri" or tanggal == "jumat"):
        tanggal = nextdayinweek(4, 0)
    elif (tanggal == "saturday" or tanggal == "sat" or tanggal == "sabtu"):
        tanggal = nextdayinweek(5, 0)
    tanggal = re.sub('\.', '/', tanggal)
    postgl = re.search('\d+/\d+/\d+', tanggal)
    if (postgl):
        return tanggal
    else:
        return "ERR"


def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


# ----


# COMMAND: REMINDER
class Reminder(commands.Cog):
    # everyone: 855701462793453578
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reminder",
                      brief="B$help reminder",
                      description="add new custom reminder")
    async def reminderbf(self, ctx, namatugas, tanggal, jam, tag):
        jam = jamFilter(jam)
        if (jam == "ERR"):
            await ctx.channel.send("salah format jam bro")
            return
        tanggal = tanggalFilter(tanggal)
        if (tanggal == "ERR"):
            await ctx.channel.send("salah format tanggal bro")
            return
        finalstr = stringDateCombine(tanggal, jam)
        if strToDate(finalstr) < datetime.datetime.now():
            await ctx.channel.send("dah lewat bro")
            return
        if (tag == "me"):
            tag = "<@{}>".format(str(ctx.message.author.id))
        if tag == "everyone":
            tag = "@everyone"
        if tag in rolelist:
            tag = "<@&{}>".format(rolelist[tag])
            # DB HERE
        remindobj = [finalstr, namatugas, tag, str(ctx.message.author.name)]
        if "reminder" in db.keys():
            dbr = db["reminder"]
            dbr.append(remindobj)
        else:
            db["reminder"] = [remindobj]
        diff = datetime.datetime.strptime(
            finalstr, "%d/%m/%Y %H:%M") - datetime.datetime.now()
        difd = diff.days
        difs = diff.seconds
        difh = math.floor(difs / 3600)
        difm = math.floor((difs % 3600) / 60)
        if difd > 25:
            deccs = "more than 25 days"
        else:
            difhh = difd * 24 + difh
            deccs = "{} hour(s) and {} minute(s)".format(difhh, difm)
        await ctx.channel.send("Reminder {} in {} for {}".format(
            namatugas, deccs, tag))

    @commands.command(name="listreminder", brief="show upcoming events")
    async def listreminderbf(self, ctx):
        now = datetime.datetime.now() + datetime.timedelta(hours=9, minutes=5)
        if "reminder" in db.keys():
            if db["reminder"]:
                # await ctx.channel.send(db["reminder"])
                counter = len(db["reminder"].value)
                if counter == 1:
                    descc = "There is {} upcoming event".format(counter)
                else:
                    descc = "There are {} upcoming events".format(counter)
                embed = discord.Embed(title="Upcoming events",
                                      description=descc,
                                      color=0x850000)
                for rm in db["reminder"]:
                    yourname = rm[2]
                    if yourname == "@everyone":
                        yourname = "everyone"
                    if yourname[0] == '<':
                        x = re.split("\@|\>", yourname)
                        if (x[1][0] == '&'):
                            for ky in rolelist:
                                if rolelist[ky] == x[1][1:]:
                                    yourname = ky
                        else:
                            yourname = await bot.fetch_user(x[1])
                    namez = "{} - {}".format(rm[1], yourname)
                    diff = datetime.datetime.strptime(
                        rm[0], "%d/%m/%Y %H:%M") - datetime.datetime.now()
                    difd = diff.days
                    difs = diff.seconds
                    difh = math.floor(difs / 3600)
                    difm = math.floor((difs % 3600) / 60)
                    if difd > 25:
                        deccs = "💤 Due in more than 25 days 💤\n"
                    else:
                        difhh = difd * 24 + difh
                        if difhh > 0:
                            deccs = "✨ Due in {} hour(s) and {} minute(s)✨\n".format(
                                difhh, difm)
                        else:
                            deccs = "💢 Due in {} hour(s) and {} minute(s)💢\n".format(
                                difhh, difm)

                    deccs += datetime.datetime.strftime(
                        datetime.datetime.strptime(rm[0], "%d/%m/%Y %H:%M") +
                        datetime.timedelta(hours=7), "%d/%m/%Y %H:%M")
                    embed.add_field(name=namez, value=deccs, inline=False)

                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send("There's no reminder at the moment!")
                await ctx.channel.send(
                    "Try adding one with this format (in GMT+7/WIB please):")
                await ctx.channel.send("B$reminder nama_tugas {} me".format(
                    datetime.datetime.strftime(now, "%d/%m/%Y %H:%M")))

        else:
            await ctx.channel.send("There's no reminder at the moment!")
            await ctx.channel.send(
                "Try adding one with this format (in GMT+7/WIB please):")
            await ctx.channel.send("B$reminder nama_tugas {} me".format(
                datetime.datetime.strftime(now, "%d/%m/%Y %H:%M")))

    @commands.command(name ="listtomorrow")
    async def listtomorrowbf(self,ctx):
        await ctx.channel.send(embed=dailyReminder(7+24))
    @commands.command(name ="listtoday")
    async def listtodaybf(self,ctx):
        await ctx.channel.send(embed=dailyReminder(7))


    @commands.command(name="undoreminder")
    async def undoreminderbf(self, ctx):
        now = datetime.datetime.now() + datetime.timedelta(hours=9, minutes=5)
        if "reminder" in db.keys():
            if db["reminder"]:
                rmdate = db["reminder"][-1][0]
                rmname = db["reminder"][-1][1]
                rmtag = db["reminder"][-1][2]
                timeindo = datetime.datetime.strftime(
                    datetime.datetime.strptime(rmdate, "%d/%m/%Y %H:%M") +
                    datetime.timedelta(hours=7), "%d/%m/%Y %H:%M")
                if (rmtag == "me"):
                    rmtag = "<@{}>".format(str(ctx.message.author.id))
                if rmtag == "everyone":
                    rmtag = "@everyone"
                if (rmtag in rolelist):
                    rmtag = "<@&{}>".format(rolelist[rmtag])
                await ctx.channel.send(
                    "Deleting {} reminder for {} at {}".format(
                        rmname, rmtag, timeindo))
                del db["reminder"][-1]
                await ctx.channel.send("Deleted! Reminder count: {}".format(
                    len(db["reminder"].value)))
            else:
                await ctx.channel.send("There's no reminder at the moment!")
                await ctx.channel.send(
                    "Try adding one with this format (in GMT+7/WIB please):")
                await ctx.channel.send("B$reminder nama_tugas {} me".format(
                    datetime.datetime.strftime(now, "%d/%m/%Y %H:%M")))
        else:
            await ctx.channel.send("There's no reminder at the moment!")
            await ctx.channel.send(
                "Try adding one with this format (in GMT+7/WIB please):")
            await ctx.channel.send("B$reminder nama_tugas {} me".format(
                datetime.datetime.strftime(now, "%d/%m/%Y %H:%M")))

bot.add_cog(Reminder(bot))

# ----


# OTHER COMMANDS
@bot.command(name="restart", brief="restart bot")
async def restartbf(ctx):
    await ctx.channel.send("Please wait...")
    restart_bot()


@bot.command(name="testdailyquote")
async def inspiretodaybf(ctx):
    await ctx.channel.send(todaysQuote())


@bot.command(name="inspire", brief="inspiration +99")
async def inspirebf(ctx):
    await ctx.channel.send(getQuote())


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


# ON MESSAGE
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

    if msg.startswith(('thanks bot', 'Thanks bot', 'Thanks Bot')):
        await message.channel.send('Your Welcome, 御主人様!')

    if msg.startswith('B$hello'):
        await message.channel.send('Hello!')

    # Reset Reminder
    if msg.startswith('B$resetreminder'):
        channel = message.channel
        await channel.send('Will delete all queries in database. Please enter `yes` in 5s to confirm')

        def check(m):
            return m.content == 'yes' and m.channel == channel

        henji = await bot.wait_for('message', check=check, timeout = 6.0)
        henji = henji
        if "reminder" in db.keys():
            cont = len(db["reminder"].value)
            del db["reminder"]
            await channel.send('Deleted {} queries.'.format(cont))
        else:
            await channel.send("Already empty")

# -----

# help Command

@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(
        title="Join our Discord",
        url="https://discord.gg/B6JRWgbf",
        description=
        "This bot is still on development, we need more feature ideas",
        color=0x43b8ea)
    embed.set_author(
        name="See Github Repo",
        url="https://github.com/danzel-py/BruhBot5555",
        icon_url="https://i.ibb.co/RzQzcMr/Git-Hub-Mark-120px-plus.png")
    embed.add_field(name="Reminder",
                    value="B$reminder\nB$listreminder\nB$listtoday\nB$listtomorrow\nB$undoreminder",
                    inline=False)
    embed.add_field(name="Other", value="B$inspire\nB$restart", inline=False)
    embed.set_footer(text="Try `B$help reminder` to add a new reminder ")
    await ctx.send(embed=embed)


@help.command()
async def reminder(ctx):
    now = datetime.datetime.now() + datetime.timedelta(hours=9, minutes=5)
    em = discord.Embed(title="B$reminder",
                       description="create a new reminder",
                       color=0x850000)
    em.add_field(
        name="**Command**",
        value="`B$reminder` `reminder_name` `dd/mm/YYYY` `HH:MM` `tags`",
        inline=False)
    em.add_field(
        name='example',
        value="B$reminder do_stuffs {} me\nB$reminder zoom_meet tomorrow 7pm me"
        .format(datetime.datetime.strftime(now, "%d/%m/%Y %H:%M")),
        inline=False)
    em.add_field(name="Key", value="Registered Channel ID", inline=True)
    roleliststr = ""
    for tagsr in rolelist:
        roleliststr += rolelist[tagsr] + ", "
    roleliststr += "everyone, me."
    em.add_field(name="Value", value="{}".format(channelint), inline=True)
    em.add_field(name="In progress:", value="Tinggal pake", inline=False)
    em.set_footer(text="note: midnight is 23:59, 12pm is invalid=>try 0am")
    await ctx.send(embed=em)


# Loops/scheduler
# b25 everyone: 855701462793453578
# ucb everyone: 855703085825785856
@tasks.loop(minutes=1)
async def remindFunction():
    print('letscheck')
    now = datetime.datetime.now()
    if "reminder" in db.keys():
        for rm in db["reminder"]:
            roleexist = -1
            roleid = 0
            print(rm[0])
            print(datetime.datetime.strftime(now, "%d/%m/%Y %H:%M"))
            stringrm = rm[0]
            daterm = strToDate(stringrm)
            datermhminus1 = daterm + datetime.timedelta(hours=-1)
            datermmminus10 = daterm + datetime.timedelta(minutes=-10)
            strhminus1 = datetime.datetime.strftime(datermhminus1,
                                                    "%d/%m/%Y %H:%M")
            strmminus10 = datetime.datetime.strftime(datermmminus10,
                                                     "%d/%m/%Y %H:%M")

            if strmminus10 == now.strftime("%d/%m/%Y %H:%M"):
                if rm[2] in rolelist:
                    roleexist = 1
                    roleid = rolelist[rm[2]]

                if roleexist != -1:
                    await bot.get_channel(channelint).send(
                        "tag: <@&{}> ".format(roleid))
                await bot.get_channel(channelint).send(
                    "🚨 Hey {} it's 10 minutes to {}. Gotta go fast!".format(
                        rm[2], rm[1]))
            if strhminus1 == now.strftime("%d/%m/%Y %H:%M"):
                if rm[2] in rolelist:
                    roleexist = 1
                    roleid = rolelist[rm[2]]

                if roleexist != -1:
                    await bot.get_channel(channelint).send(
                        "tag: @<&{}> ".format(roleid))
                await bot.get_channel(channelint).send(
                    "Hey {} it's 1 hour to {}.".format(rm[2], rm[1]))
            if rm[0] == now.strftime("%d/%m/%Y %H:%M"):
                if rm[2] in rolelist:
                    roleexist = 1
                    roleid = rolelist[rm[2]]

                if roleexist != -1:
                    await bot.get_channel(channelint).send(
                        "tag: @&{} ".format(roleid))
                await bot.get_channel(channelint).send(
                    "Hey {} it's time to {}.".format(rm[2], rm[1]))

            elif strToDate(rm[0]) < now:
                db["reminder"].remove(rm)
                print("dah lewat")
    else:
        return


@tasks.loop(hours=1)
async def dailyQuotes():
    print('getting quotes...')
    now = datetime.datetime.now()
    sixaclock = now.replace(hour=21, minute=0, second=0, microsecond=0)
    sevenaclock = now.replace(hour=22, minute=0, second=0, microsecond=0)
    if (now < sevenaclock and now > sixaclock):
        em = dailyReminder(7)
        await bot.get_channel(channelint).send(embed=em)
        await bot.get_channel(channelint).send(todaysQuote())


#-6.915055499431372, 107.59463161394709

my_secret = os.environ['TOKEN']

keep_alive()  # AUTO PING
bot.run(my_secret)
