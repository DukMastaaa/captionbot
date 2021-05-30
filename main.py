import io
import os
import discord
import requests  # not good
from discord.ext import commands
from PIL import Image

import image_captioner as captioner

bot = commands.Bot(command_prefix=".")


@bot.event
async def on_ready():
    print("I'm online as", bot.user)


@bot.command(
    brief="makes you a sussy baka",
    help="there is a dumos amugos"
)
async def amogus(ctx):
    await ctx.channel.send("when the impostor is sus!")


@bot.command(
    brief="very sussy",
    help="red is sus"
)
async def crewmate(ctx):
    with open("crewmate.png", "rb") as file:
        discord_file = discord.File(file)
    await ctx.send(file=discord_file)


@bot.command(
    brief="reverses stuff"
)
async def reverse(ctx, *, something: str):
    await ctx.channel.send(something[::-1])


@bot.command()
async def image(ctx, top_text: str, bottom_text: str):
    attachments = ctx.message.attachments
    if not attachments:
        return
    
    url = attachments[0].url
    image = Image.open(requests.get(url, stream=True).raw)
    
    captioner.add_captions_to_image(image, top_text, bottom_text)

    with io.BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png')) 


token = os.getenv("DISCORD_BOT_TOKEN")
bot.run(token)