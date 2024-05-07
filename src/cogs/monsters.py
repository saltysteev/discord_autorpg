"""
monsters.py
"""

import datetime
import random

import discord
from discord.ext import commands

from utils import config as cfg
from utils.db import Player

from bot import AutoBot

utc = datetime.timezone.utc
raidtime = datetime.time(hour=14, minute=0, tzinfo=utc)

monster_list = [
    "Rabid Rat",
    "Sickly Goblin",
    "Overgrown Radish",
    "Spirit of Kunzile",
    "Tomatoe",
    "Mangy Dog",
    "Ungulating Mass",
    "Plant Overgrowth",
    "Doppleganger",
    "Screeching Parrot",
    "Angry Hobo",
    "Professional Amateur",
    "Sadistic Sadist",
    "Enduring Procrastinator",
    "Convention Furry",
    "Claw-clacking Crabs",
    "Gilded Dragon",
    "Opportunistic Thief",
    "Banded Warband",
    "Grandma",
    "Hungry Hematoads",
    "Bee",
    "Lopsided Logger",
]


class Monsters(commands.Cog):
    """Handler of monster combat"""

    def __init__(self, bot: AutoBot):
        self.bot = bot

    async def encounter(self, player: Player):
        """Monster encounter"""

        def get_dps(p) -> int:
            t = 0
            for i in p:
                if isinstance(i[1], dict):
                    t += i[1]["dps"]
            return t

        p_max = get_dps(player)
        m_max = random.randint(p_max - 500, p_max + 250)
        if m_max <= 0:
            m_max = 1
        monster = random.choice(monster_list)
        monster_level = random.randint(player.level - 10, player.level + 20)
        smite_chance = True if random.random() <= 0.10 and player.align == 1 else False
        player_score = (
            random.randint(1, p_max)
            if not smite_chance
            else random.randint(1, p_max * 2)
        )
        monster_score = random.randint(1, m_max)
        alvar = 90 if player.align == 1 else 100
        val = int((random.randint(4, 6)) / alvar * (player.nextxp - player.currentxp))
        embed = discord.Embed(color=discord.Color(cfg.COLOR_MONSTER))
        embed.set_thumbnail(url=player.avatar_url)
        embed.title = f":crossed_swords: {player.name} [{player_score}/{p_max}] came upon a Lv{monster_level} {monster} [{monster_score}/{m_max}] in the wild and drew their weapon!"
        if smite_chance:
            embed.add_field(
                name="",
                value=f"**{player.name}'s good nature appeases the Gods and they cast SMITE!**",
                inline=False,
            )
        if player_score >= monster_score:
            player.nextxp -= val
            if player.nextxp - player.currentxp < 0:
                player.nextxp = player.currentxp + 1
            embed.add_field(
                name="",
                value=f"They challenged the monster and valiantly defeated the beast, boosting them **{self.bot.ctime(val)}** towards level {player.level + 1}!\n"
                f"They now reach the next level in **{self.bot.ctime(player.nextxp - player.currentxp)}**",
            )
        else:
            player.nextxp += val
            player.totalxplost += val
            embed.add_field(
                name="",
                value=f"They challenged the monster and was heroicly bested in combat, slowing them **{self.bot.ctime(val)}** from level {player.level + 1}!\n"
                f"They now reach the next level in **{self.bot.ctime(player.nextxp - player.currentxp)}**",
            )
        if player.optin:
            await self.bot.game_channel.send(f"<@!{player.uid}>", embed=embed) # type: ignore
        else:
            await self.bot.game_channel.send(embed=embed) # type: ignore


async def setup(bot):
    await bot.add_cog(Monsters(bot))
