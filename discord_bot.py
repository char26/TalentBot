import os
import discord
from dotenv import load_dotenv
import json
from wowhead_bis import best_gear, best_talents, available_slots, available_bosses

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
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
    is_boss = False
    username = message.author.name + '#' + message.author.discriminator

    if "$$" in message.content:
        cont = message.content.split("$$")[1].split(" ")[0]

        for boss in available_bosses:
            if cont in boss:
                is_boss = True
                break

    if message.author == client.user:
        return
    
    if message.content == "$$slots":
        await message.channel.send(available_slots)
    
    # example: $$del Monk Wind-Raid
    elif "$$del" in message.content:
        spec_build_to_delete = message.content.split("$$del ")[1]
        class_ = spec_build_to_delete.split(" ")[0].capitalize()
        build_to_delete = spec_build_to_delete.split(" ")[1]

        all_builds[username].pop(class_)

        with open("builds.json", "w") as f:
            json.dump(all_builds, f)

        await message.channel.send(f"Deleted {build_to_delete} from your builds.")

    elif '$$my-builds' in message.content:
        your_builds = ""
        class_ = message.content.split("$$my-builds ")[1].capitalize()
        try:
            for i in range(len(all_builds[username][class_]["build_name"])):
                your_builds += all_builds[username][class_]["build_name"][i] + "\n" + all_builds[username][class_]["build_string"][i] + "\n" + f'<https://www.wowhead.com/talent-calc/blizzard/{all_builds[username][class_]["build_string"][i]}>' + "\n-------------------------------------------------------------------------------------------------------\n\n"
            await message.channel.send(your_builds)
        except KeyError:
            await message.channel.send(f"No builds for {class_}.")
        

    elif message.content == "$$help":
        await message.channel.send("https://github.com/char26/TalentBot")

    elif "$$save" in message.content:
        command = message.content.split("$$save")[1].split(" ")
        class_ = command[1].capitalize()
        build_name = command[2]
        build_string = command[3]
        if build_name in all_builds[username][class_]["build_name"]:
            await message.channel.send(f"Name already in use. $$del {build_name}, or use a different name.")
        else:
            try:
                all_builds[username][class_]["build_name"].append(build_name)
                all_builds[username][class_]["build_string"].append(build_string)

            except KeyError:
                all_builds[username][class_] = {"build_name": [build_name], "build_string": [build_string]}
    
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
            msg = await message.channel.send(info + "\n\n React with ✅ to save this to '$$my-builds'.")
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
    
    if "React with ✅" in reaction.message.content:
        if emoji == "✅":
            build_string = reaction.message.content.split("\n\n")[1]
            build_name = reaction.message.content.split("-")[1].split(" ")[0] + "-" + reaction.message.content.split("-")[3]
            class_ = reaction.message.content.split("-")[1].split(" ")[1].capitalize()

            try:
                if build_name in all_builds[username][class_]["build_name"]:
                    await reaction.message.channel.send(f"Build name already in use. $$del {build_name} then react again.")
                else:
                    all_builds[username][class_]["build_name"].append(build_name)
                    all_builds[username][class_]["build_string"].append(build_string)

            except KeyError:
                all_builds[username][class_] = {"build_name": [build_name], "build_string": [build_string]}
    
            with open("builds.json", "w") as f:
                json.dump(all_builds, f)

@client.event
async def on_reaction_remove(reaction, user):
    global all_builds
    username = user.name + '#' + user.discriminator

    emoji = reaction.emoji

    if user.bot:
        return
    
    if "React with ✅ " in reaction.message.content:
        if emoji == "✅":
            build_name = reaction.message.content.split("-")[1].split(" ")[0] + "-" + reaction.message.content.split("-")[3]
            class_ = reaction.message.content.split("-")[1].split(" ")[1].capitalize()
            
            index = all_builds[username][class_]["build_name"].index(build_name)

            all_builds[username][class_]["build_name"].pop(index)
            all_builds[username][class_]["build_string"].pop(index)

            with open("builds.json", "w") as f:
                json.dump(all_builds, f)

client.run(TOKEN)