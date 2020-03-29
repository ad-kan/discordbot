import discord
import time
import requests
from discord.ext import commands

weather_api = 'http://api.openweathermap.org/data/2.5/weather?appid='
bot = commands.Bot(command_prefix = '!')

@bot.event #Bot ready, presence
async def on_ready(channel):
    print('Bot is ready yo.')
    await bot.change_presence(activity=discord.Game(name='(!) god'))
    channel = bot.get_channel(693871505783914537)
    await channel.send('The bot is ready')

@bot.event #Welcome
async def on_member_join(member):
    print(f'{member} joined')
    await ctx.send(f'Welcome to the server, **@{member}**!')

@bot.event #Goodbye
async def on_member_remove(member):
    print(f'{member} left')
    await ctx.send(f'Goodbye, **@{member}**!')

@bot.command() #Ping
async def ping(ctx):
    await ctx.send(f'Pong! The latency is **{round(bot.latency*1000)}ms**')

@bot.command() #Calc Help
async def calchelp(ctx):
    await ctx.send('Format: !calc Operation|First Number|Second Number (Key: 1 for addition, 2 for subtraction, 3 for multiplication, 4 for division)')

@bot.command()
async def corona(ctx):
    await ctx.send('No, sorry')

@bot.command() #Calculator
async def calc(ctx,num1,option,num2):
    result = 0
    num1 = float(num1)
    num2 = float(num2)
    if option == 'plus' or option == '+':
        result = num1 + num2
    if option == 'minus' or option == '-':
        result = num1 - num2
    if option == 'times' or option == '*':
        result = num1 * num2
    if option == 'divided' or option == '/':
        result = num1 / num2
    
    print('Option is ' + str(option))
    
    await ctx.send(str(result))

@bot.command()
async def purge(ctx,amount=5):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(str(amount) + ' messages were cleared successfuly.')
    time.sleep(2)
    await ctx.channel.purge(limit=1)

@bot.command()
async def a(ctx):
    print(ctx.message)

@bot.command()
async def weather(ctx,city):
    url = weather_api + city
    
    json_data = requests.get(url).json()
    temperature = (json_data['main']['temp']-273)
    description = json_data['weather'][0]['main']

    await ctx.send('The weather in **' + city.capitalize() + '** is ' + description + '.')
    await ctx.send('The temperature is ' + str(round(temperature,2)))

#Weather API key:

bot.run('')