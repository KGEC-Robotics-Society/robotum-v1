#============================================= All imports
import datetime
import discord,requests, sys, webbrowser, bs4
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter
from discord.flags import Intents
import os
import discord
import random
import requests
from io import BytesIO
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import *
from discord.ext.commands import Bot

#============================================= Intents
intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.message_content = True
robotum = commands.Bot(command_prefix=".", intents=intents, help_command=None)
clients = discord.Client(intents=intents)

#============================================= If bot online it will print bot is online on console
@robotum.event
async def on_ready():
    print('We have logged in as {0.user}'.format(robotum))

#============================================= Checking bot is working or not
@robotum.command()                                       
async def hello(ctx):
    await ctx.send(f"Hello @{ctx.author}")
    member = ctx.author
    await ctx.send(member.avatar.url)

#============================================= Member join welcome embed
@robotum.event
async def on_member_join(member):
    channel = robotum.get_channel(869448970416582746)
    embed=discord.Embed(title="𝓦𝓮𝓵𝓬𝓸𝓶𝓮!",description=f"{member.mention} Just Joined The Server.")
    img = Image.open("Images/download.png")
    if member.avatar == None:
        font = ImageFont.truetype("ttf/KaushanScript-Regular.ttf", 75)
        font2 = ImageFont.truetype("ttf/KaushanScript-Regular.ttf", 80)

        text="Welcome"

        draw=ImageDraw.Draw(img)
        draw.text((600,100), text, (255, 255, 255), font=font, align='center')
        draw.text((300,300), f"{member}", (255, 255, 255), font=font2, align='center' )
        img.save("Images/text.png")
        file = discord.File("Images/text.png", filename="Welcome.png")
        embed.set_image(url="attachment://Welcome.png")
        embed.timestamp = datetime.datetime.now()
    else:
        response = requests.get(member.avatar.url)
        img2 = Image.open(BytesIO(response.content))
        img2 = img2.resize((350,350))
        mask_im = Image.new("L", (img2.width,img2.height), 0)
        draw2 = ImageDraw.Draw(mask_im)
        center_x, center_y = (175, 175)
        radius = 122.5
        left = center_x - radius
        top = center_y - radius
        right = center_x + radius
        bottom = center_y + radius
        circle_box = [(left, top), (right, bottom)]
        draw2.ellipse(circle_box, fill=255)
        blur = mask_im.filter(ImageFilter.GaussianBlur(10))
        img.paste(img2, (575, 0), blur)

        font = ImageFont.truetype("ttf/KaushanScript-Regular.ttf", 75)
        font2 = ImageFont.truetype("ttf/KaushanScript-Regular.ttf", 80)
        # Image.Image.paste(img,img2,(575,10), ())

        text="Welcome"

        draw=ImageDraw.Draw(img)
        draw.text((600,300), text, (255, 255, 255), font=font, align='center')
        draw.text((300,400), f"{member}", (255, 255, 255), font=font2, align='center' )

        img.save("Images/text.png")
        file = discord.File("Images/text.png", filename="Welcome.png")
        embed.set_image(url="attachment://Welcome.png")
        # embed.set_thumbnail(url=member.avatar.url)
        embed.timestamp = datetime.datetime.now()
        print (member)
    await channel.send(file=file, embed=embed)
    await member.send("Welcome to the Official KGEC Robotics Society Discord Server! \n\nThis is Robotum, the official bot of the server. We are glad that you joined us! 🤗 \n Please Check rules and information in the Server")
    # await channel.send(member.avatar)

#============================================= Member left embed
@robotum.event
async def on_member_remove(member:discord.member):
    channel = robotum.get_channel(869448970416582746)
    embed=discord.Embed(title="🥹",description=f"{member.mention} Just Left The Server.")
    embed.timestamp = datetime.datetime.now()
    await channel.send(embed=embed)
    

#============================================= Fetching token from .env
load_dotenv()
robotum.run(os.getenv("TOKEN"))