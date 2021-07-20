import discord
from replit import db
import math
import datetime
import re
from discord.ext import commands
from functions.reminderfun import jamFilter, tanggalFilter, stringDateCombine, strToDate, dailyReminder
from constants import rolelist


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
                            yourname = await self.bot.fetch_user(x[1])
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

    @commands.command(name="listtomorrow")
    async def listtomorrowbf(self, ctx):
        await ctx.channel.send(embed=dailyReminder(7 + 24))

    @commands.command(name="listtoday")
    async def listtodaybf(self, ctx):
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
