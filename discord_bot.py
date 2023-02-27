import os
import discord
from dotenv import load_dotenv
import json
from wowhead_bis import best_gear, best_talents, available_slots, available_bosses

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
    global all_builds
    global is_boss
    username = message.author.name + '#' + message.author.discriminator

    for boss in available_bosses:
        if (message.content.split("$$")[1].split(" ")[0]) in boss:
            is_boss = True
            break

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
        await message.channel.send("https://github.com/char26/TalentBot")

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

    elif ('$$raid' in message.content) or ('$$mplus' in message.content) or (is_boss == True):
        command = message.content.split("$$")[1].split(" ")
        content = command[0]
        spec_class = command[1]
        slot = command[2]

        if slot == 'talents':
            info = best_talents(content, spec_class)
            msg = await message.channel.send(info + "\n\n React with ✅ to save this to your builds.")
            await msg.add_reaction("✅")
        else:
            info = best_gear(content, spec_class, slot)
            await message.channel.send(f"```{info}```")

@client.event
async def on_reaction_add(reaction, user):
    global all_builds
    username = user.name + '#' + user.discriminator

    emoji = reaction.emoji

    if user.bot:
        return
    
    if "React with ✅ to save this to your builds." in reaction.message.content:
        if emoji == "✅":
            build_string = reaction.message.content.split("\n\n")[1]
            build_name = reaction.message.content.split("-")[1].split(" ")[0] + "-" + reaction.message.content.split("-")[3]
            
            try:
                all_builds[username]["build_name"].append(build_name)
                all_builds[username]["build_string"].append(build_string)

            except KeyError:
                all_builds.update({username: {"build_name": [build_name], "build_string": [build_string]}})
    
            with open("builds.json", "w") as f:
                json.dump(all_builds, f)

client.run(TOKEN)