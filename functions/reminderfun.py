import re
import datetime
from replit import db
import discord
from constants import rolelist

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
                description="We have {} reminder(s) {}.".format(ct,tpll),
                color=0x99ff00)
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
                                  description="No upcoming events for {}.".format(tpll),color=0x99ff00)
    else:
        embed = discord.Embed(title="{}'s REMINDER".format(tplx),
                              description="No upcoming events for {}.".format(tpll),color=0x99ff00)
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
    now = datetime.datetime.now() + datetime.timedelta(hours = 7)
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
