#============================================= All imports
import datetime
import discord,requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import random
import pymongo
import discord.utils
from io import BytesIO
from dotenv import load_dotenv
from discord.ext import commands
# from discord.ext import *
# from discord.ext.commands import Bot
from keep_alive import keep_alive

#============================================= Intents
intents = discord.Intents.all()
intents.members = True
intents.presences = True
intents.message_content = True
robotum = commands.Bot(command_prefix=".", intents=intents, help_command=None)
clients = discord.Client(intents=intents)

#============================================= Connecting to MongoDB
uri = os.getenv("MONGOTOKEN")
client = pymongo.MongoClient(uri)
mydb = client["discord"]
mycol = mydb["member_roles"]

#============================================= If bot online it will print bot is online on console
@robotum.event
async def on_ready():
    print('We have logged in as {0.user}'.format(robotum))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    

#============================================= Checking bot is working or not
@robotum.command()                                       
async def hello(ctx):
    await ctx.send(f"Hello @{ctx.author}")

#============================================= Member join welcome embed
@robotum.event
async def on_member_join(member):
    channel = robotum.get_channel(917788968618168356)
    embed=discord.Embed(title="𝓦𝓮𝓵𝓬𝓸𝓶𝓮!",description=f"{member.mention} Just Joined The Server.")
    backgrounds =os.listdir('Images')
    random_bg = random.choice(backgrounds)
    img = Image.open("Images/" + random_bg)
    # print(random_bg)
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
        radius = 160
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
        text="Welcome"
        draw=ImageDraw.Draw(img)
        draw.text((600,300), text, (255, 255, 255), font=font, align='center')
        draw.text((300,400), f"{member}", (255, 255, 255), font=font2, align='center' )
        img.save("Images/text.png")
        file = discord.File("Images/text.png", filename="Welcome.png")
        embed.set_image(url="attachment://Welcome.png")
        embed.timestamp = datetime.datetime.now()
        print (member)
    await channel.send(file=file, embed=embed)
    await member.send("Welcome to the Official KGEC Robotics Society Discord Server! \n\nThis is Robotum, the official bot of the server. We are glad that you joined us! 🤗 \n Please Check rules and information in the Server")

#============================================= Member left embed
@robotum.event
async def on_member_remove(member:discord.member):
    channel = robotum.get_channel(918388896042209290)
    embed=discord.Embed(title="🥹",description=f"{member.mention} Just Left The Server.")
    embed.timestamp = datetime.datetime.now()
    await channel.send(embed=embed)

#============================================= Giving role to member
@robotum.command()                                       
async def verify(ctx): 
    print(ctx.author)
    
    dbrole = mycol.find_one({"discoid" : str(ctx.author.id)})
    dbrole2 = mycol.find_one({"discoid" : str(ctx.author)})
    if dbrole == None and dbrole2 == None:
        await ctx.send("Please copy your discord id and paste it on link and scan your qrcode. After scan you can give .verify command to get role. Link=")
    elif dbrole == None:
        await ctx.send(f"Hello @{ctx.author} Your roles are updated. Please check it out")
        if dbrole2.get("app") == "yes":
            app = discord.utils.get(ctx.guild.roles, name="App Development") 
            await ctx.author.add_roles(app)
        if dbrole2.get("iot") == "yes":
            iot = discord.utils.get(ctx.guild.roles, name="Internet Of Things(IoT)") 
            await ctx.author.add_roles(iot)
        if dbrole2.get("ml") == "yes":
            ml = discord.utils.get(ctx.guild.roles, name="Machine Learning") 
            await ctx.author.add_roles(ml)
        if dbrole2.get("cloud") == "yes":
            cloud = discord.utils.get(ctx.guild.roles, name="Cloud Computing") 
            await ctx.author.add_roles(cloud)
        if dbrole2.get("mecatronics") == "yes":
            mechatronics = discord.utils.get(ctx.guild.roles, name="Mechatronics") 
            await ctx.author.add_roles(mechatronics)
        if dbrole2.get("web") == "yes":
            web = discord.utils.get(ctx.guild.roles, name="Web Development") 
            await ctx.author.add_roles(web)
        if dbrole2.get("design") == "yes":
            design = discord.utils.get(ctx.guild.roles, name="Design Team") 
            await ctx.author.add_roles(design)
        if dbrole2.get("video") == "yes":
            video = discord.utils.get(ctx.guild.roles, name="Video Editor") 
            await ctx.author.add_roles(video)
        if dbrole2.get("content") == "yes":
            content = discord.utils.get(ctx.guild.roles, name="Content Writer") 
            await ctx.author.add_roles(content)
            
    elif dbrole2 == None:
        await ctx.send(f"Hello @{ctx.author} Your roles are updated. Please check it out")
        if dbrole.get("app") == "yes":
            app = discord.utils.get(ctx.guild.roles, name="App Development") 
            await ctx.author.add_roles(app)
        if dbrole.get("iot") == "yes":
            print("yes")
            iot = discord.utils.get(ctx.guild.roles, name="Internet Of Things(IoT)") 
            await ctx.author.add_roles(iot)
        if dbrole.get("ml") == "yes":
            ml = discord.utils.get(ctx.guild.roles, name="Machine Learning") 
            await ctx.author.add_roles(ml)
        if dbrole.get("cloud") == "yes":
            cloud = discord.utils.get(ctx.guild.roles, name="Cloud Computing") 
            await ctx.author.add_roles(cloud)
        if dbrole.get("mecatronics") == "yes":
            mechatronics = discord.utils.get(ctx.guild.roles, name="Mechatronics") 
            await ctx.author.add_roles(mechatronics)
        if dbrole.get("web") == "yes":
            web = discord.utils.get(ctx.guild.roles, name="Web Development") 
            await ctx.author.add_roles(web)
        if dbrole.get("design") == "yes":
            design = discord.utils.get(ctx.guild.roles, name="Design Team") 
            await ctx.author.add_roles(design)
        if dbrole.get("video") == "yes":
            video = discord.utils.get(ctx.guild.roles, name="Video Editor") 
            await ctx.author.add_roles(video)
        if dbrole.get("content") == "yes":
            content = discord.utils.get(ctx.guild.roles, name="Content Writer") 
            await ctx.author.add_roles(content)


#============================================= Fetching token from .env
load_dotenv()
keep_alive()
robotum.run(os.getenv("TOKEN"))