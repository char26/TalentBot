import os
import discord
from dotenv import load_dotenv
import json
from prettytable import PrettyTable
from wowhead_bis import best_gear, best_talents, available_slots

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all() #was .default()
intents.messages = True

client = discord.Client(intents=intents)

with open("builds.json", "r") as f:
    all_builds = json.load(f)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    print(
        f'{client.user} is connected!'
    )

@client.event
async def on_message(message):
    username = message.author.name + '#' + message.author.discriminator
    global all_builds

    if message.author == client.user:
        return
    
    if message.content == "$$slots":
        await message.channel.send(available_slots)
    
    # example: $$del Wind-Raid
    elif "$$del" in message.content:
        build_to_delete = message.content.split("$$del ")[1]
        index = all_builds[username]["build_name"].index(build_to_delete)

        all_builds[username]["build_name"].pop(index)
        all_builds[username]["build_string"].pop(index)

        with open("builds.json", "w") as f:
            json.dump(all_builds, f)

        await message.channel.send(f"Deleted {build_to_delete} from your builds.")

    elif message.content == "$$my-builds":
        your_builds = ""
        for i in range(len(all_builds[username]["build_name"])):
            your_builds += all_builds[username]["build_name"][i] + "\n" + all_builds[username]["build_string"][i] + "\n" + f'https://www.wowhead.com/talent-calc/blizzard/{all_builds[username]["build_string"][i]}' + "\n-------------------------------------------------------------------------------------------------------\n\n"

        await message.channel.send(your_builds)

    elif message.content == "$$help":
        await message.channel.send("format as: $$content spec-class slot\n\nfor example:\n$$raid havoc-demon-hunter waists")

    elif "$$save" in message.content:
        command = message.content.split("$$save")[1].split(" ")
        build_name = command[1]
        build_string = command[2]

        try:
            all_builds[message.author.name + '#' + message.author.discriminator]["build_name"].append(build_name)
            all_builds[message.author.name + '#' + message.author.discriminator]["build_string"].append(build_string)

        except KeyError:
            all_builds.update({username: {"build_name": [build_name], "build_string": [build_string]}})
 
        with open("builds.json", "w") as f:
            json.dump(all_builds, f)

        await message.channel.send("Saved build. Type $$my-builds to see all of your saved builds.")

# Keep as last
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