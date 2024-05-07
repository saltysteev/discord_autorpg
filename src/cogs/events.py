"""
events.py
"""

import random

import discord
from discord.ext import commands

from utils import config as cfg
from utils.db import Player
from utils.loot import get_item

from bot import AutoBot


class Events(commands.Cog):
    """Handler of events"""

    def __init__(self, bot: AutoBot):
        super().__init__()
        self.bot = bot

    async def randomevent(self, player: Player):
        """Runs when a player succeeds in a random event chance"""
        event_choice = random.choices(
            ["gevent", "bevent", "hog"], weights=[70, 25, 5], cum_weights=None, k=1
        )
        alvar = 90 if player.align == 1 else 100
        val = int((random.randint(4, 6) / alvar) * (player.nextxp - player.currentxp))
        em = discord.Embed(color=discord.Color(cfg.COLOR_EVENT))
        em.set_thumbnail(url=player.avatar_url)
        if event_choice[0] == "gevent":  # Good
            player.nextxp -= val
            if player.nextxp - player.currentxp < 0:
                player.nextxp = player.currentxp + 1
            event = random.choice(self.bot.readfile("gevents"))
            em.title = f":zap: {player.name} {event}!"
            em.add_field(
                name="",
                value=f"This wonderous event has boosted them **{self.bot.ctime(val)}** towards level **{player.level + 1}**.\n"
                f"They now reach the next level in **{self.bot.ctime(player.nextxp - player.currentxp)}**",
            )
        elif event_choice[0] == "bevent":  # Bad
            player.nextxp += val
            player.totalxplost += val
            event = random.choice(self.bot.readfile("bevents"))
            em.title = f":zap: {player.name} {event}!"
            em.add_field(
                name="",
                value=f"This unfortunate event has slowed them **{self.bot.ctime(val)}** towards level **{player.level + 1}**.\n"
                f"They now reach the next level in **{self.bot.ctime(player.nextxp - player.currentxp)}**",
            )
        elif event_choice[0] == "hog":  # Lucky
            val = int(int(10 + random.randint(1, 8)) / alvar * player.nextxp)
            player.nextxp -= val
            if player.nextxp - player.currentxp < 0:
                player.nextxp = player.currentxp + 1
            em.title = (
                f":zap: Blessed! {player.name} has been touched by the Hand of Law!"
            )
            em.add_field(
                name="",
                value=f"This very rare event has boosted them **{self.bot.ctime(val)}** towards level **{player.level + 1}**.\n"
                f"They now reach the next level in **{self.bot.ctime(player.nextxp - player.currentxp)}**",
            )
        else:
            print("Something went wrong choosing a random event")
        item = await get_item(player)
        em.add_field(
            name=f"{player.name} also found some new loot!",
            value=self.bot.item_string(item[0]),
            inline=False,
        )
        footer = (
            f"This {item[1]} is stronger, so they equipped the new one!"
            if item[2]
            else f"This {item[1]} is weaker, so they tossed it away."
        )
        em.set_footer(text=footer)
        if player.optin:
            await self.bot.guild.system_channel.send(f"<@!{player.uid}>", embed=em)  # type: ignore
        else:
            await self.bot.guild.system_channel.send(embed=em)  # type: ignore


async def setup(bot):
    """Cog setup"""
    await bot.add_cog(Events(bot))
