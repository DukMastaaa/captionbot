import discord
import os
# from PIL import Image, ImageFont, ImageDraw

client = discord.Client()

@client.event
async def on_ready():
    print("I'm in")
    print(client.user)

@client.event
async def on_message(message):
    if message.author != client.user:
        await message.channel.send(message.content[::-1])

token = os.getenv("DISCORD_BOT_TOKEN")
client.run(token)