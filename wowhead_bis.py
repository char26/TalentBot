from bs4 import BeautifulSoup
import requests
import re
import numpy as np
from prettytable import PrettyTable

available_slots = ['weapons', 'trinkets', 'head', 'neck', 'shoulder', 'back', 'chest', 'wrist', 'hands', 'waists', 'legs', 'feet', 'rings']
available_specs = [
    'blood-death-knight', 'frost-death-knight', 'unholy-death-knight',
    'havoc-demon-hunter', 'vengeance-demon-hunter',
    'balance-druid', 'feral-druid', 'guardian-druid', 'restoration-druid',
    'beast-mastery-hunter', 'marksmanship-hunter', 'survival-hunter',
    'arcane-mage', 'fire-mage', 'frost-mage',
    'brewmaster-monk', 'mistweaver-monk', 'windwalker-monk',
    'holy-paladin', 'protection-paladin', 'retribution-paladin',
    'discipline-priest', 'holy-priest', 'shadow-priest',
    'assassination-rogue', 'outlaw-rogue', 'subtlety-rogue',
    'elemental-shaman', 'enhancement-shaman', 'restoration-shaman',
    'affliction-warlock', 'demonology-warlock', 'destruction-warlock',
    'arms-warrior', 'fury-warrior', 'protection-warrior'
]



def best_gear(raid_mplus, spec_class, slot):
    wowhead_links = []
    clean_wh_links = []
    gear_names = []

    # Getting the best-in-slot items from mplus-subcreation.net
    ########################################### For All Slots
    if slot == 'all':
        pass # Maybe one day

    ########################################### For Specific Slots
    elif (spec_class in available_specs) and (slot in available_slots):
        if raid_mplus == 'mplus':
            subcreation_link = f"https://{raid_mplus}.subcreation.net/{spec_class}.html#{slot}"
        elif raid_mplus =='raid':
            subcreation_link = f"https://{raid_mplus}.subcreation.net/vault-{spec_class}.html#{slot}"
        page = requests.get(subcreation_link)

        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id = f"table-spec-{slot}")

        best_gear = results.find_all("a", href=True)

        for x in best_gear[0:2]:
            wowhead_links.append(re.findall('".*"', str(x)))

        if ['"https://www.wowhead.com/item=0"'] in wowhead_links:
            wowhead_links.pop(1)
        elif 'warcraftlogs' in wowhead_links[1][0]:
            wowhead_links.pop(1)

        wowhead_links = np.concatenate(wowhead_links)
        
        for x in wowhead_links:
            clean_wh_links.append(eval(x))

        # Parsing Wowhead for item info
        for x in clean_wh_links:
            wowhead_html = requests.get(x)
            wowhead_soup = BeautifulSoup(wowhead_html.content, 'html.parser')

            gear_names.append(wowhead_soup.find("h1", class_="heading-size-1").text)

        # Outputting to ascii table
        x = PrettyTable()
        x.field_names = ["Item", "Slot", "Wowhead Link"]

        for i in range(len(gear_names)):
            x.add_row([gear_names[i], slot.capitalize(), clean_wh_links[i]])

        return x

##################################################### For talents
def best_talents(raid_mplus, spec_class):
    # Getting talent string
    if raid_mplus == 'mplus':
        subcreation_link = f"https://{raid_mplus}.subcreation.net/{spec_class}.html#top"
    elif raid_mplus == 'raid':
        subcreation_link = f"https://{raid_mplus}.subcreation.net/vault-{spec_class}.html#top"
    page = requests.get(subcreation_link)

    soup = BeautifulSoup(page.content, 'html.parser')

    talent_builds = soup.find_all("a", title="open wowhead talent calculator")

    wowhead_links = []
    wowhead_links.append(re.findall('"https://www.wowhead.com/talent-calc/blizzard/.*"', str(talent_builds[0])))
    talent_string = str(wowhead_links[0]).split('"https://www.wowhead.com/talent-calc/blizzard/')[1].split('" target="_blank"')[0]

    
    talent_link = "https://www.wowhead.com/talent-calc/blizzard/" + talent_string
    best_build = f"Top talent build on subcreation for {spec_class} in {raid_mplus}:\n\n{talent_string}\n\n{talent_link}"
    
    return best_build