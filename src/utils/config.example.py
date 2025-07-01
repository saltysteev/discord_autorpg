"""
config.py
"""

# Debug switch, changes the database to a fallback mode
DEBUG = False
# Game version
VERSION = "3.4.0"

# Game info - displayed when a player uses /info
GAME_INFO = f"```AutoRPG (v{VERSION}) - by steev | https://autorpg.deadnet.org/```"
# Game website URL - also used in a player's profile link. Do not use a trailing slash!
GAME_URL = "https://autorpg.deadnet.org"

# Guild ID, grabbed from Discord
GUILD_ID = 0
# The unique Discord token
DISCORD_TOKEN = "token here"
# Discord application ID, grabbed from Discord
APPLICATION_ID = 0
# List of discord user ID's separated by a comma who have access to admin commands
SERVER_ADMINS = [261960455369523201]
# Main game channel ID that posts all player level ups/events/etc
GAME_CHANNEL = 0
# The interval in which the game loops (in seconds)
INTERVAL = 5
# The base time to level in seconds, 600 seconds = 10 minutes (base * (exp ** current level))
TIME_BASE = 600
# Exponential rewards and penalties are strange percentages relevant to 100%
# For example a quest_reward is 0.90 meaning 10%, while a quest_penalty is 1.05 meaning 5%
# The exponential increase in time to next level when someone levels up (base * (exp ** curent level))
TIME_EXP = 1.16
# Quest reward: how much to remove from the player's next level up (time to next level * quest reward)
QUEST_REWARD = 0.90
# Quest penaly: how much to add to the player's next level up (time to next level * quest penalty)
QUEST_PENALTY = 1.05
# Size of the map grid that players traverse across during their adventure (X,Y)
MAP_SIZE = [1000, 1000]
# Enable or disable PVP, some people might be in low population servers or wish to have this off
ENABLE_COMBAT = True
# Minimum level a player has to be to be randomly selected as a challenger
MIN_CHALLENGE_LEVEL = 25
# Name of weapon slots
WEAPON_SLOTS = [
    "weapon",
    "shield",
    "helmet",
    "chest",
    "gloves",
    "boots",
    "ring",
    "amulet",
]
# Current holiday, this changes the file that is loaded for events and bosses
# HOLIDAY_LIST is a list of the names of the holidays. This also tells the bot what folder the events are in
# For example, if Christmas is selected, it reads ./txtfiles/christmas/
# This is for when you want to make custom holidays - just make sure the folder names match what's in the list
# 0 = None
# 1 = Christmas
# 2 = Halloween
HOLIDAY = 0
HOLIDAY_LIST = [
    "christmas",
    "halloween",
]

# Discord embed colors
COLOR_COMBAT = 0x990000
COLOR_LEVELUP = 0xFFE100
COLOR_EVENT = 0xFFFFFF
COLOR_MONSTER = 0x000000
COLOR_QUEST = 0x49AA2C

# Tips
TIPS = [
    "After level 10, you can change your class using /setjob! It is purely cosmetic and can be anything, but may be renamed if deemed offensive.",
    "Want to get alerted when an event happens to you? Use /alert to enable it (or disable it!)",
    "Good aligned players get a 10% boost to equipment and good events!",
    "Good aligned players have a chance to **Smite**, doubling their chance of victory in monster encounters!",
    # "Evil aligned players get a 10% penalty to equipment but have the chance to steal from others on victories!",
    "Evil aligned players have a chance to **Backstab**, doubling their chance of victory in duels!",
    "You can change your alignment and class at any time!",
    "Item rarity affect the power of that item, and makes you stronger (or weaker) in duels!",
    "While you may have a shiny Legendary weapon, it will eventually be replaced. New item drops scale with your own level!",
]

# Database Config
DBTYPE = "mysql"
DBUSER = "user"
DBPASS = "pass"
DBHOST = "localhost"
DBPORT = 3306
DBNAME = "autorpg"
