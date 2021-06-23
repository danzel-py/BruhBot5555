import requests
import json
import discord
import datetime

def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def todaysQuote():
    response = requests.get("https://zenquotes.io/api/today")
    json_data = json.loads(response.text)
    quote = json_data[
        0]['q'] + " \n\n-" + json_data[0]['a']
    embed=discord.Embed(description="{}".format(quote),color=0xff4000)
    return (embed)

def todaysWeather():
    response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=-6.915439850489121&lon=107.59349662423351&exclude=hourly,minutely&units=metric&appid=7f21efc3bc3d18d7afe91adcde35f8fe")
    json_data = json.loads(response.text)
    today = json_data["daily"][0]
    cloudiness = today["clouds"]
    pop = today["pop"]
    pop = pop*100
    feelslike = today["feels_like"]
    uvi = today["uvi"]
    unix = today["dt"]
    flmorn = feelslike["morn"]
    flday = feelslike["day"]
    fleve = feelslike["eve"]
    flnight = feelslike["night"]
    tmpmax = today["temp"]["max"]
    tmpmin = today["temp"]["min"]
    mainw = today["weather"][0]["main"]
    desc = today["weather"][0]["description"]
    icon = today["weather"][0]["icon"]
    hum = today["humidity"]
    uvi = today["uvi"]
    embed=discord.Embed(title="{}".format(mainw), description="{} with {}% probability of precipitation".format(desc,pop),color=0x20c9df)
    embed.set_author(name="Today's Weather")
    embed.set_thumbnail(url="http://openweathermap.org/img/wn/{}@2x.png".format(icon))
    embed.add_field(name="Cloudiness", value="Humidity\nMax UV index\nMax Temp\nMin Temp", inline=True)
    embed.add_field(name="{}%".format(cloudiness), value="{}%\n{}\n{}°C\n{}°C".format(uvi,hum,tmpmax,tmpmin), inline=True)
    unixint = int(unix)
    utcstr = datetime.datetime.utcfromtimestamp(unixint).strftime("%d %b %y at %H:%M")
    embed.set_footer(text="Ts: {}\nLoc: Binus Bandung".format(utcstr))
    return embed
