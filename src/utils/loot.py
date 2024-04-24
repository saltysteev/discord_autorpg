"""
loot.py
"""

import math
import random
from enum import Enum

from utils.config import WEAPON_SLOTS
from utils.db import Player

conditions = [
    {"name": "Wretched", "weight": 0.14, "mdps": 0.6, "rank": 0},
    {"name": "Poor", "weight": 0.23, "mdps": 1, "rank": 0},
    {"name": "Worn", "weight": 0.50, "mdps": 1, "rank": 0},
    {"name": "Refurbished", "weight": 0.45, "mdps": 1.3, "rank": 0},
    {"name": "Dusty", "weight": 0.4, "mdps": 1.5, "rank": 1},
    {"name": "Clean", "weight": 0.45, "mdps": 2, "rank": 1},
    {"name": "Polished", "weight": 0.34, "mdps": 2.5, "rank": 2},
    {"name": "Pristine", "weight": 0.17, "mdps": 3, "rank": 3},
    {"name": "Displayed", "weight": 0.1, "mdps": 3.5, "rank": 4},
    {"name": "God-touched", "weight": 0.03, "mdps": 5, "rank": 5},
]
qualities = [
    {"name": "Basic", "weight": 0.85, "mdps": 1, "rank": 0},
    {"name": "Feeble", "weight": 0.35, "mdps": 0.6, "rank": 0},
    {"name": "Cracked", "weight": 0.35, "mdps": 0.6, "rank": 0},
    {"name": "Weathered", "weight": 0.42, "mdps": 1.1, "rank": 1},
    {"name": "Rusted", "weight": 0.31, "mdps": 1.1, "rank": 0},
    {"name": "Bolstered", "weight": 0.27, "mdps": 1.3, "rank": 1},
    {"name": "Veteran", "weight": 0.24, "mdps": 1.7, "rank": 1},
    {"name": "Gilded", "weight": 0.18, "mdps": 2.8, "rank": 2},
    {"name": "Pristine", "weight": 0.14, "mdps": 3.5, "rank": 2},
    {"name": "Authentic", "weight": 0.1, "mdps": 4, "rank": 3},
    {"name": "Illustrious", "weight": 0.02, "mdps": 7, "rank": 3},
    {"name": "Ascended", "weight": 0.01, "mdps": 10, "rank": 4},
    {"name": "Galactic", "weight": 0.005, "mdps": 12, "rank": 5},
]
prefixes = [
    {"name": "", "weight": 0.9, "mgold": 1, "mdps": 1},
    {"name": "Burning ", "weight": 0.82, "mgold": 1, "mdps": 1.15},
    {"name": "Blazing ", "weight": 0.65, "mgold": 1.15, "mdps": 1.25},
    {"name": "Smoldering ", "weight": 0.47, "mgold": 1.25, "mdps": 1.35},
    {"name": "Cold ", "weight": 0.82, "mgold": 1.25, "mdps": 1.15},
    {"name": "Chilled ", "weight": 0.65, "mgold": 1.25, "mdps": 1.25},
    {"name": "Frozen ", "weight": 0.53, "mgold": 1.25, "mdps": 1.25},
    {"name": "Glacial ", "weight": 0.45, "mgold": 1.25, "mdps": 1.25},
    {"name": "Keen ", "weight": 0.65, "mgold": 1.25, "mdps": 1.15},
    {"name": "Accurate ", "weight": 0.64, "mgold": 1.25, "mdps": 1.25},
    {"name": "Sharp ", "weight": 0.6, "mgold": 1.25, "mdps": 1.35},
    {"name": "Fatal ", "weight": 0.22, "mgold": 1.25, "mdps": 1.25},
    {"name": "Deadly ", "weight": 0.15, "mgold": 1.25, "mdps": 1.25},
    {"name": "Sturdy ", "weight": 0.37, "mgold": 1.25, "mdps": 1.15},
    {"name": "Quick ", "weight": 0.26, "mgold": 1.25, "mdps": 1.25},
    {"name": "Swift ", "weight": 0.34, "mgold": 1.25, "mdps": 1.35},
    {"name": "Solid ", "weight": 0.45, "mgold": 1.25, "mdps": 1.25},
    {"name": "Rigid ", "weight": 0.62, "mgold": 1.25, "mdps": 1.25},
    {"name": "Focused ", "weight": 0.32, "mgold": 1.25, "mdps": 1.15},
    {"name": "Centered ", "weight": 0.24, "mgold": 1.25, "mdps": 1.15},
    {"name": "Holy ", "weight": 0.1, "mgold": 1.25, "mdps": 2},
    {"name": "Lightforged ", "weight": 0.1, "mgold": 1.25, "mdps": 2},
]
suffixes = [
    {"name": "", "weight": 0.9, "mgold": 1, "mdps": 1},
    {"name": " of the Bear", "weight": 0.1, "mgold": 1.25, "mdps": 1.25},
    {"name": " of the Soldier", "weight": 0.1, "mgold": 1.35, "mdps": 1.35},
    {"name": " of the Demented", "weight": 0.1, "mgold": 1.95, "mdps": 1.95},
    {"name": " of the Damned", "weight": 0.1, "mgold": 1, "mdps": 1.3},
    {"name": " of the Cursed", "weight": 0.1, "mgold": 1, "mdps": 1.3},
    {"name": " of the Kindled", "weight": 0.1, "mgold": 1, "mdps": 2},
    {"name": " of the Gods", "weight": 0.1, "mgold": 1, "mdps": 1.95},
    {"name": " of the Bold", "weight": 0.1, "mgold": 1, "mdps": 1.2},
    {"name": " of Nightmares", "weight": 0.1, "mgold": 1, "mdps": 1.5},
    {"name": " of Dreams", "weight": 0.1, "mgold": 1, "mdps": 1.5},
    {"name": " of the Tortured", "weight": 0.1, "mgold": 1, "mdps": 1.6},
    {"name": " of the Forgotten", "weight": 0.1, "mgold": 1, "mdps": 1.6},
    {"name": " of Kunzile", "weight": 0.1, "mgold": 1, "mdps": 2.5},
    {"name": " of Glory", "weight": 0.1, "mgold": 1, "mdps": 1.4},
    {"name": " of Shame", "weight": 0.1, "mgold": 1, "mdps": 1.9},
    {"name": " of Sin", "weight": 0.1, "mgold": 1, "mdps": 1.8},
]
shields = [
    {"name": "Shield", "weight": 0.9, "bdps": 2, "bgold": 100},
    {"name": "Heater Shield", "weight": 0.6, "bdps": 2, "bgold": 100},
    {"name": "Buckler", "weight": 0.7, "bdps": 2, "bgold": 100},
    {"name": "Kite Shield", "weight": 0.7, "bdps": 2, "bgold": 100},
    {"name": "Bouche Shield", "weight": 0.6, "bdps": 2, "bgold": 100},
    {"name": "Targe", "weight": 0.4, "bdps": 2, "bgold": 100},
    {"name": "Fluted Buckler", "weight": 0.4, "bdps": 2, "bgold": 100},
    {"name": "Lionheart Shield", "weight": 0.3, "bdps": 2, "bgold": 100},
    {"name": "Pavis", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Warrior Shield", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Creased Shield", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Viking Shield", "weight": 0.4, "bdps": 2, "bgold": 100},
    {"name": "Rondache Shield", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Round Shield", "weight": 0.7, "bdps": 2, "bgold": 100},
    {
        "name": "Aegis",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"It\'s signed "To Athena" and it\'s quite charred."',
    },
    {
        "name": "Achilles' Shield",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"The Earth, sky and sea, the sun, the moon and the constellations"',
    },
]
helmets = [
    {"name": "Helmet", "weight": 0.9, "bdps": 2, "bgold": 100},
    {"name": "Kettle Hat", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Great Helm", "weight": 0.6, "bdps": 2, "bgold": 100},
    {"name": "Sallet", "weight": 0.4, "bdps": 2, "bgold": 100},
    {"name": "Bascinet", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Barbuta", "weight": 0.6, "bdps": 2, "bgold": 100},
    {"name": "Aventail", "weight": 0.6, "bdps": 2, "bgold": 100},
    {"name": "Norman Helmet", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Crusader Helm", "weight": 0.7, "bdps": 2, "bgold": 100},
    {
        "name": "Helm of Awe",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"Glittering worm, thy hissing was great..."',
    },
]
chests = [
    {"name": "Chestplate", "weight": 0.9, "bdps": 2, "bgold": 100},
    {"name": "Gambeson", "weight": 0.6, "bdps": 2, "bgold": 100},
    {"name": "Plate Armor", "weight": 0.6, "bdps": 2, "bgold": 100},
    {"name": "Brigandine", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Cuirass", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Chainmail", "weight": 0.7, "bdps": 2, "bgold": 100},
    {
        "name": "Beowulf's Armor",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"If death does take me, send the hammered mail of my armor to Higlac"',
    },
]
gloves = [
    {"name": "Gloves", "weight": 0.8, "bdps": 2, "bgold": 100},
    {"name": "Gauntlets", "weight": 0.7, "bdps": 2, "bgold": 100},
    {"name": "Finger Gloves", "weight": 0.6, "bdps": 2, "bgold": 100},
    {"name": "Knuckles", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Claws", "weight": 0.2, "bdps": 2, "bgold": 100},
]
boots = [
    {"name": "Boots", "weight": 0.9, "bdps": 2, "bgold": 100},
]
rings = [
    {"name": "Ring", "weight": 0.9, "bdps": 2, "bgold": 100},
]
amulets = [
    {"name": "Amulet", "weight": 0.9, "bdps": 2, "bgold": 100},
]
weapons = [
    {"name": "Sword", "weight": 0.9, "bdps": 2, "bgold": 100},
    {"name": "Hammer", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Claymore", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Longsword", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Greatsword", "weight": 0.2, "bdps": 2, "bgold": 100},
    {"name": "Broadsword", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Katana", "weight": 0.15, "bdps": 2, "bgold": 100},
    {"name": "Cutlass", "weight": 0.15, "bdps": 2, "bgold": 100},
    {"name": "Sabre", "weight": 0.4, "bdps": 2, "bgold": 100},
    {"name": "Axe", "weight": 0.9, "bdps": 2, "bgold": 100},
    {"name": "Battle-axe", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Greataxe", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Dagger", "weight": 0.9, "bdps": 2, "bgold": 100},
    {"name": "Bollock Dagger", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Dirk", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Trench Knife", "weight": 0.43, "bdps": 2, "bgold": 100},
    {"name": "Stiletto", "weight": 0.24, "bdps": 2, "bgold": 100},
    {"name": "Corvo", "weight": 0.18, "bdps": 2, "bgold": 100},
    {"name": "Spear", "weight": 0.9, "bdps": 2, "bgold": 100},
    {"name": "Lance", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Polearm", "weight": 0.5, "bdps": 2, "bgold": 100},
    {"name": "Halberd", "weight": 0.24, "bdps": 2, "bgold": 100},
    {"name": "Glaive", "weight": 0.23, "bdps": 2, "bgold": 100},
    {"name": "Scythe", "weight": 0.1, "bdps": 2, "bgold": 100},
    {
        "name": "Law's Retribution",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"The weight of sin heavily draws this dagger to the ground."',
    },
    {
        "name": "Fate's End",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"You call out for mercy, but there is no answer."',
    },
    {
        "name": "Tyrfing",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"Do not touch this cursed blade, for it only seeks death."',
    },
    {
        "name": "Surtr",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"A red glow surrounds this blade, and it\'s too hot to hold."',
    },
    {
        "name": "Excalibur",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"The lady of the lake calls this blade\'s name. You should return it."',
    },
    {
        "name": "Harpe",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"Patricide is a sin, oh heavenly one."',
    },
    {
        "name": "Zulfiqar",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"There is no sword but the Zulfiqar, and there is no hero but Ali."',
    },
    {
        "name": "Gramr",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"The bark of a tree still clings to the blade. Odin would be pleased."',
    },
    {
        "name": "Masamune",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"This sword, inscribed with the letters HONJO, emits an eerie cry."',
    },
    {
        "name": "Muramasa",
        "weight": 0.01,
        "bdps": 4,
        "flair": '"As you hold this weapon, you feel the urge to test it\'s sharpness on your friends."',
    },
]


class Slots(Enum):
    weapon = weapons
    shield = shields
    helmet = helmets
    chest = chests
    glove = gloves
    boot = boots
    ring = rings
    amulet = amulets


async def weighted_choice(items):
    """Choose items based on weight"""

    def weight(arr):
        return [item for obj in arr for item in [obj] * int(obj["weight"] * 100)]

    return random.choice(weight(items))


async def get_item(player: Player):
    """Generates and returns a randomized item"""

    async def generate_item(equip_list):
        base = await weighted_choice(equip_list)
        prefix = await weighted_choice(prefixes)
        suffix = await weighted_choice(suffixes)
        quality = await weighted_choice(qualities)
        condition = await weighted_choice(conditions)
        rank = quality["rank"] + condition["rank"]
        match rank:
            case 1 | 2:
                rankrole = "Uncommon"
            case 3 | 4:
                rankrole = "Rare"
            case 5 | 6:
                rankrole = "Epic"
            case 7 | 8:
                rankrole = "Legendary"
            case 9:
                rankrole = "Ascended"
            case _:
                rankrole = "Common"
        dps = math.floor(
            (
                random.randrange(base["bdps"] - 1, base["bdps"] + 1)
                * math.sqrt(
                    (
                        prefix["mdps"]
                        + suffix["mdps"]
                        + quality["mdps"]
                        + condition["mdps"]
                    )
                    * 1.2
                    + 1
                )
                * player.level
            )
        )
        flair = base["flair"] if "flair" in base else None
        generated_item = {
            "name": base["name"],
            "quality": quality["name"],
            "condition": condition["name"],
            "prefix": prefix["name"],
            "suffix": suffix["name"],
            "dps": dps,
            "rank": "Unique" if "flair" in base else rankrole,
            "flair": flair,
        }
        return generated_item

    slot = random.choice(list(Slots))
    item = await generate_item(slot.value)
    replaced_item: bool = False

    if item["dps"] > player.slot.name["dps"]:
        await player.update(weapon=item, _columns=["weapon"])
        replaced_item = True

    return item, slot, replaced_item
