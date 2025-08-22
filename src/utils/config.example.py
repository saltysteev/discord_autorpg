"""
config.py
"""

#########################################################################
#   REQUIRED CONFIGURATIONS
#########################################################################
# The unique Discord token
DISCORD_TOKEN = "TOKEN_HERE"
# Game name
GAME_NAME = "AutoRPG"
# Game version
VERSION = "3.5.0"
# Game info - displayed when a player uses /info. Uses Discord markdown formatting
GAME_INFO = f"```{GAME_NAME} (v{VERSION}) - by steev | https://deadnet.org/```"
# Game website URL - also used in a player's profile link. NOTICE: Do not use a trailing slash!
GAME_URL = "https://autorpg.deadnet.org"
# Guild ID, grabbed from Discord
GUILD_ID = 0
# Discord application ID, grabbed from Discord
APPLICATION_ID = 0
# List of discord user ID's separated by a comma who have access to admin commands
SERVER_ADMINS = [261960455369523201]
# Main game channel ID that posts all player level ups/events/etc
GAME_CHANNEL = 0
# Channel ID for misc activies like quests, raids, etc
ANNOUNCE_CHANNEL = 0
# Database configuration
# DBTYPE must match your database type and async (postgres, sqlite, etc)
# See https://collerek.github.io/ormar/latest/install/#database-backend for more informatoin
DBTYPE = "mysql+aiomysql"
DBUSER = "user"
DBPASS = "pass"
DBHOST = "localhost"
DBPORT = 3306
DBNAME = "autorpg"

#########################################################################
#   OPTIONAL CONFIGURATIONS
#########################################################################
# Debug switch, changes the database to a fallback mode
DEBUG = False
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
# Time in seconds that a player needs to idle to get a loot token
TOKEN_TIME = 43200  # 12 hours

# TODO: Simplify this mess
# Current holiday, this changes the file that is loaded for events and bosses
# HOLIDAY is current index of HOLIDAY_LIST which is list of the names of the holidays.
# This also tells the bot what folder the events are in
# For example, if Christmas is selected, it reads ./txtfiles/christmas/
# When you want to make custom holidays - just make sure the folder names match what's in the list
# 0 = Normal / no holiday
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
COLOR_LOOT = 0xA000FF

# Application emojis
# Emojis used in /profile are pulled from Discord so you don't need to have them in your server
# However, if you want to use custom emojis, replace the names and IDs with your own.
E_WEAPON = "<:weapon:1390359056836989040>"
E_SHIELD = "<:shield:1390358010744012870>"
E_HELMET = "<:helm:1390357866371616828>"
E_CHEST = "<:chest:1390357529296633877>"
E_GLOVES = "<:gloves:1390357819097878600>"
E_BOOTS = "<:boots:1390357641653653627>"
E_RING = "<:ring:1390357474543931502>"
E_AMULET = "<:amulet:1390357952539660418>"
E_UPGRADE = "<:upgrade:1408143066426118234>"
