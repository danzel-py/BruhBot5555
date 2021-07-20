import discord
from replit import db
from keep_alive import keep_alive
import sys
import os
import datetime
from discord.ext import tasks
from functions.reminderfun import dailyReminder, strToDate
from functions.tablerfun import tablerFunction
from functions.weatherquotefun import todaysQuote, todaysWeather, getQuote
from functions.instagramfun import getNewPost
from cogs.Reminder import Reminder
from constants import rolelist, channelint, bot
# from emoji import UNICODE_EMOJI
# from discord.utils import get
# import asyncio

# BUG tagged as #broken

# FUNCTIONS


def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)


# ----

# COMMAND: REMINDER

bot.add_cog(Reminder(bot))

# ----


# OTHER COMMANDS
@bot.command(name="restart", brief="restart bot")
async def restartbf(ctx):
    await ctx.channel.send("Please wait...")
    restart_bot()


@bot.command(name="testdailyquote")
async def inspiretodaybf(ctx):
    await ctx.channel.send(embed=todaysQuote())


@bot.command(name="inspire", brief="inspiration +99")
async def inspirebf(ctx):
    await ctx.channel.send(getQuote())


@bot.command(name="weathertoday")
async def wtodaybf(ctx):
    await ctx.channel.send(embed=todaysWeather())


# ----


# ON READY
@bot.event
async def on_ready():
    if "reminder" in db.keys():
        print(db["reminder"])
    remindFunction.start()
    dailyQuotes.start()
    igUpdate.start()
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

    if msg.startswith("getfoo"):
        memid = message.author.id
        membr = message.guild.get_member(memid)
        foorole = discord.utils.get(message.guild.roles, name="fooRole")
        await membr.add_roles(foorole)
        await message.channel.send("Assigned fooRole to {}".format(membr))
    if msg.startswith("delfoo"):
        memid = message.author.id
        membr = message.guild.get_member(memid)
        foorole = discord.utils.get(message.guild.roles, name="fooRole")
        await membr.remove_roles(foorole)
        await message.channel.send("Deleted fooRole from {}".format(membr))

    if msg.startswith(('thanks bot', 'Thanks bot', 'Thanks Bot')):
        await message.channel.send('Your Welcome, 御主人様!')

    if msg.startswith('B$hello'):
        await message.channel.send('Hello!')

    # Reset Reminder
    if msg.startswith('B$resetreminder'):
        channel = message.channel
        await channel.send(
            'Will delete all queries in database. Please enter `yes` in 5s to confirm'
        )

        def check(m):
            return m.content == 'yes' and m.channel == channel

        henji = await bot.wait_for('message', check=check, timeout=6.0)
        henji = henji
        if "reminder" in db.keys():
            cont = len(db["reminder"].value)
            del db["reminder"]
            await channel.send('Deleted {} queries.'.format(cont))
        else:
            await channel.send("Already empty")

    # tabler
    if msg.startswith('B$table'):
        content = message.content
        await message.channel.send("```" + tablerFunction(content) + "```")


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
    embed.add_field(
        name="Reminder",
        value=
        "B$reminder\nB$listreminder\nB$listtoday\nB$listtomorrow\nB$undoreminder",
        inline=False)
    embed.add_field(name="Table", value="B$table", inline=False)
    embed.add_field(name="Weather", value="B$weathertoday", inline=False)
    embed.add_field(name="Other", value="B$inspire\nB$restart", inline=False)
    embed.set_footer(text="Try `B$help reminder` to add a new reminder")
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
    em.add_field(name="In progress:",
                 value="idk mo nambah fitur ap lagi",
                 inline=False)
    em.set_footer(
        text="note: midnight is 23:59 but 12pm is invalid so try 0am")
    await ctx.send(embed=em)


# Loops/scheduler
# b25 everyone: 855701462793453578
# ucb everyone: 855703085825785856
@tasks.loop(minutes=1)
async def remindFunction():
    print('checking reminder...')
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

@tasks.loop(minutes = 5)
async def igUpdate():
    Robj = getNewPost('binus_bandung',os.environ['igsid'])
    if(Robj):
        post_type = 'image'
        if Robj['is_video']:
            post_type = 'video'

        em=discord.Embed(title="See original post in instagram", url = Robj['post_url'],description="binus_bandung has just posted a new {}!".format(post_type))
        em.set_image(url=Robj['display_url'])
        print(Robj)
        em.set_footer(text="posted: {}\nfetched: {}".format((Robj['taken_at_timestamp']+datetime.timedelta(hours=7)).strftime("%d-%m-%Y %H:%M:%S"),(datetime.datetime.now() + datetime.timedelta(hours = 7)).strftime("%d-%m-%Y %H:%M:%S")))
        await bot.get_channel(channelint).send(embed = em)
    

@tasks.loop(hours=1)
async def dailyQuotes():
    print('getting quotes...')
    now = datetime.datetime.now()
    sixaclock = now.replace(hour=21, minute=0, second=0, microsecond=0)
    sevenaclock = now.replace(hour=22, minute=0, second=0, microsecond=0)
    if (now < sevenaclock and now > sixaclock):
        em = dailyReminder(7)
        await bot.get_channel(channelint).send(embed=todaysWeather())
        await bot.get_channel(channelint).send(embed=em)
        await bot.get_channel(channelint).send(embed=todaysQuote())


#-6.915055499431372, 107.59463161394709

my_secret = os.environ['TOKEN']

keep_alive()  # AUTO PING
bot.run(my_secret)
