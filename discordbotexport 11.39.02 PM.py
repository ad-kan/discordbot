from __future__ import print_function
import discord
from discord import File
from PIL import Image
import pytesseract
import time
import requests
from discord.ext import commands
import imgkit
import matplotlib
import json

#Dominant color
import numpy
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import binascii
import struct

#Nutritionix
from nutritionix import Nutritionix

coronavirus_api = 'https://api.covid19api.com/summary'
nutrition_api = 'https://api.nutritionix.com/v1_1/search/'
bot = commands.Bot(command_prefix = '!')

@bot.event #Bot ready, presence
async def on_ready():
    print('Bot is ready yo.')
    await bot.change_presence(activity=discord.Game(name='(!) god'))
    channel = bot.get_channel(693871505783914537)
    await channel.send('The bot is ready')

@bot.event #Welcome
async def on_member_join(member):
    print(f'{member} joined')
    channel = bot.get_channel(693871505783914537)
    await channel.send(f'Welcome to the server, **@{member}**!')

@bot.event #Goodbye
async def on_member_remove(member):
    print(f'{member} left')
    channel = bot.get_channel(693871505783914537)
    await channel.send(f'Goodbye, **@{member}**!')

@bot.command() #Ping
async def ping(ctx):
    await ctx.send(f'Pong! The latency is **{round(bot.latency*1000)}ms**')

@bot.command() #Calc Help
async def calchelp(ctx):
    await ctx.send('Format: !calc Operation|First Number|Second Number (Key: 1 for addition, 2 for subtraction, 3 for multiplication, 4 for division)')

@bot.command()
async def dm(ctx):
    channel = bot.get_member(305784264140652554)
    await channel.send(305784264140652554, "test")

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
    if option == 'raised to' or option == '^':
        result = int(num1)^int(num2)
    
    print('Option is ' + str(option))
    
    await ctx.send(str(result))

@bot.command()
async def purge(ctx,amount=5):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(str(amount) + ' messages were cleared successfuly.')
    time.sleep(2)
    await ctx.channel.purge(limit=1)

@bot.command()
async def weather(ctx,city):
    url = weather_api + city
    
    json_data = requests.get(url).json()
    temperature = (json_data['main']['temp']-273)
    description = json_data['weather'][0]['main'].lower()
    wthumbnail = "https://img-s-msn-com.akamaized.net/tenant/amp/entityid/BB10dsot.img?h=0&w=720&m=6&q=60&u=t&o=f&l=f"
    if "cloud" in description:
        wthumbnail = "https://media.discordapp.net/attachments/693827825756667946/695879222362898442/AkxtiBTSm_3Q_-nWDkNyywEof_yNkQWYPaS957rwnPyGoOaMrJtS2G55-08VY9E7Q6pOaf-nLHpA04o-9zblOYvIYzhQzY8Nrw.png"
    if "sun" in description:
        wthumbnail = "https://media.discordapp.net/attachments/693827825756667946/695876219488698428/sun.png"
    if "rain" in description:
        wthumbnail = "https://media.discordapp.net/attachments/693827825756667946/695879967661096960/pnkcE-iPN_EhlcxGijka6woEL9tWEz_cGerveuXP2m6dxmZ4bVH_YrB9Ud67UD0tn2lGkksmMIlxEEYhf30gEtRc69Z5qtxgvw.png"    

    embed=discord.Embed(title="Weather in Bangalore", color=0x00a3ff)
    embed.set_thumbnail(url=wthumbnail)
    embed.add_field(name="Status", value=description.capitalize(), inline=False)
    embed.add_field(name="Temperature", value=str(round(temperature,2)) + " °C", inline=False)
    await ctx.send(embed=embed)

#Weather API key: 27e72a5a2553c2aadde0508dd4487833

@bot.command()
async def corona(ctx):
    url = 'https://api.covid19api.com/summary'
    json_data = requests.get(url).json()

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    channel = bot.get_channel(693871505783914537)
    await channel.send('Shutting down.')
    print ('Bot is done yo.')
    await ctx.bot.logout()

@bot.command()
async def ocr(ctx):
    stime = time.time() #start time, end time, processing time
    await ctx.message.attachments[0].save("/home/ubuntu/cache/temp.png")
    url = ctx.message.attachments[0].url
    img = Image.open("/home/ubuntu/cache/temp.png")
    text = pytesseract.image_to_string(img, lang = 'eng')
    textsplit = text.split()
    textlen = len(text)
    etime = time.time()
    ptime = etime-stime
    
    embed = discord.Embed(title="*Result:* " + textsplit[0]+" "+textsplit[1]+" "+textsplit[2]+"...", color=0x9800ff, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    embed.set_thumbnail(url=url)
    embed.add_field(name="Text",value=text, inline=False)
    embed.add_field(name="Word count", value=str(textlen), inline=False)
    embed.add_field(name="Processing time", value=str(round(ptime,3))+" seconds", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def profile(ctx, member: discord.Member = None):
    message = await ctx.send("Processing...")
    if member is None:
        name = str(ctx.author.name)
        if str(ctx.author.nick) == 'None':
            nick = str(ctx.author.name)
        else:
            nick = str(ctx.author.nick)
        await ctx.author.avatar_url_as(format='jpg').save('/home/ubuntu/cache/userimg.jpg')
    else:
        name = str(member.name)
        if str(member.nick) == 'None':
            nick = str(member.name)
        else:
            nick = str(member.nick)
        await member.avatar_url_as(format='jpg').save('/home/ubuntu/cache/userimg.jpg')

    #color color start
    NUM_CLUSTERS = 5

    print('reading image')
    im = Image.open('/home/ubuntu/cache/userimg.jpg')
    im = im.resize((150, 150))      # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

    index_max = numpy.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    index_max = numpy.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    index_max = numpy.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    print('most frequent is %s (#%s)' % (peak, colour))
    #color color end

    invcolor = []
    invrgb = []

    for x in peak:
        invcolor.append((255-x)/255)

    invhex = matplotlib.colors.to_hex(invcolor)

    await message.edit(content="Rendering...")

    imgkitoptions = {
    'format': 'png',
    'width': '640',
    'height': '480'}

    htmlf = open('/home/ubuntu/cache/user.html','w')
    htmlf.write(f'''
    <HTML>
        <body style="background-image: -webkit-linear-gradient(#''' + colour + ''', #2c2f33)"><font face = "Avenir">
	        <H1>
                <center><font color = "''' + invhex + '''" face = "Avenir"><b>''' + nick + '''</b> </font>
	        </H2>
	        <H3>
                <center><font color = "#fff" <b>''' + name + ''' </b><br> </font>
	        </H3>
        </font><center>
        <img src="/home/ubuntu/cache/userimg.jpg" alt="" height = 150 width = 150/>
    </HTML>
    ''')
    htmlf.close()
    imgkit.from_file(['/home/ubuntu/cache/user.html'], '/home/ubuntu/cache/imgkit.png',options=imgkitoptions)
    
    await message.edit(content="Uploading...")
    await ctx.send(file=File('/home/ubuntu/cache/imgkit.png'))
    await message.delete()

@bot.command()
async def nutrient(ctx,query):
    search = nix.search(query)
    results = search.json()

    #id = results["hits"][0]["_id"]

    final = nix.item(id=results["hits"][0]["_id"]).json()
    
    embed=discord.Embed(title=(query.lower()).title(), color=0xffc300)
    embed.add_field(name="**Calories**", value=final["nf_calories"], inline=True)
    embed.add_field(name="**Total fat**", value=final["nf_total_fat"], inline=True)
    embed.add_field(name="Saturated Fat", value=final["nf_saturated_fat"], inline=True)
    embed.add_field(name="Trans fatty acid", value=final["nf_trans_fatty_acid"], inline=True)
    embed.add_field(name="Polyunsaturated fat", value=final["nf_polyunsaturated_fat"], inline=True)
    embed.add_field(name="Monounsaturated fat", value=final["nf_monounsaturated_fat"], inline=True)
    embed.add_field(name="**Cholestrol**", value=final["nf_cholesterol"], inline=True)
    embed.add_field(name="Sodium", value=final["nf_sodium"], inline=True)
    embed.add_field(name="Total carbohydrates", value=final["nf_total_carbohydrate"], inline=True)
    embed.add_field(name="Dietary fiber", value=final["nf_dietary_fiber"], inline=True)
    embed.add_field(name="Sugars", value=final["nf_sugars"], inline=True)
    embed.add_field(name="Protein", value=final["nf_protein"], inline=True)
    embed.add_field(name="Vitamin A", value=final["nf_vitamin_a_dv"], inline=True)
    embed.add_field(name="Vitamin C", value=final["nf_vitamin_c_dv"], inline=True)
    embed.add_field(name="Iron", value=final["nf_iron_dv"], inline=True)
    embed.set_footer(text="Data pulled from Nutritionix API")
    await ctx.send(embed=embed)

    with open('/home/ubuntu/cache/results.json','w') as data:
        json.dump(final,data,indent=1)

