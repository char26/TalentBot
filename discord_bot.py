import os
import discord
from dotenv import load_dotenv

from wowhead_bis import best_gear, best_talents, available_slots

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all() #was .default()
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$$help'):
        await message.channel.send("format as: $$content spec-class slot\n\nfor example:\n$$raid havoc-demon-hunter waists")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "$$slots":
        await message.channel.send(available_slots)
    elif message.content.startswith('$$'):
        command = message.content.split("$$")[1].split(" ")
        content = command[0]
        spec_class = command[1]
        slot = command[2]

        if slot == 'talents':
            info = best_talents(content, spec_class)
            await message.channel.send(info)
        else:
            info = best_gear(content, spec_class, slot)
            await message.channel.send(f"```{info}```")

client.run(TOKEN)