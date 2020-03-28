import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print('Bot is ready yo.')

@bot.event
async def on_member_join(member):
    print(f'{member} joined')

@bot.event
async def on_member_remove(member):
    print(f'{member} left')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! The latency is {round(bot.latency*1000)}ms')

@bot.command()
async def calchelp(ctx):
    await ctx.send('Format: !calc Operation|First Number|Second Number (Key: 1 for addition, 2 for subtraction, 3 for multiplication, 4 for division)')

@bot.command()
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
bot.run('NjkzMTA5MzI2NzM4NDg5NDI0.Xn4Siw.C9xL0mDXFodfsP1wEYzoGtKau9Y')