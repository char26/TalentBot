# TalentBot

Still under development, but this is a Discord bot made for myself and my friends in our private server. This bot is not available to join other servers, but the source code is here if you would like to use it yourself.

The bot has 3 main functions:
- Retrieving "best-in-slot" gear for any specialization and class in raid or mythic+ keystones.
- Retrieve best talent builds for any raid boss encounter, or mythic+ in general.
- Save talent builds, both suggested by the retrieval tool, or by inputting the name and string manually.

It scrapes data from a World of Warcraft website called 'subcreation' raid.subcreation.net, which automatically updates the most common gear and talents for each class in the game. After scraping the gear or talent build, the bot scrapes the name and other information from Wowhead.

## Instructions for using the bot
All commands start with '$$'.

### Best-in-slot

$$content spec-class slot

The example below returns the best weapons for Shadow Priest in mythic+:
$$mplus shadow-priest weapons

Here are the arguments for each part of the command:
content
- mplus (returns top gear for overall mythic+ dungeons)
- raid (returns top gear for general use in raid)

spec-class
- Self explanatory, but use a dash instead of a space for classes or specs with spaces
- For example: beast-mastery-hunter or unholy-death-knight

slot
- examples: weapons, neck, waists, head, trinkets
- type $$slots for a list of all available slots


### Talents

$$content spec-class talents

The example below returns the best talent build for a Fire Mage on Dathea, Ascended:
$$dathea fire-mage talents

Here are the arguments for each part of the command:
content
- mplus (returns top talent build for overall mythic+ dungeons)
- raid (returns top talent build for general use in raid, not recommended - use next option)
- boss (this returns the top talent build for the specific boss encounter)
  - examples: terros, sennarth, eranog, dathea, etc.
  
spec-class
- Self explanatory, but use a dash instead of a space for classes or specs with spaces
- For example: beast-mastery-hunter or unholy-death-knight

talents
- Do not change, this is part of the command.

### Save talents

$$save class build-name build-string

Example saving a build for Fire Mage in Raid:
$$save Mage Fire-Raid B8DAAAAAAAAAAAAAAAAAAAAAAkkAhWiESSBk0SIiISCAAAAAAAAAOABSEKJJSSkkkkUAAAA

Here are the arguments for each part of the command:
save
- Do not change, used to initialize the saved string.

build-name
- What you would like to name the build. No two builds can have the same name.

class
- Saves talents under that class' builds.
- Example: Mage, Priest, Warrior, DeathKnight

build-string
- The talent calculator string from wowhead.

### View talent builds

Use '$$my-builds class' to view previously saved builds.

### Delete talent build

$$del class build-name

Example:
$$del Mage Fire-Raid

### Help

$$help

Takes you back here :)
