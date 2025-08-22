"""
events.py
"""

import random

import discord
from discord.ext import commands

import utils.config as cfg
import utils.strings as s
from bot import AutoBot
from utils.db import Player
from utils.loot import get_item


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
            em.title = s.NORM_EVENT_TITLE % (player.name, event)
            em.add_field(
                name="",
                value=s.NEW_EVENT
                % (
                    self.bot.ctime(val),
                    player.level + 1,
                    self.bot.ctime(player.nextxp - player.currentxp),
                ),
            )
        elif event_choice[0] == "bevent":  # Bad
            player.nextxp += val
            player.totalxplost += val
            event = random.choice(self.bot.readfile("bevents"))
            em.title = s.NORM_EVENT_TITLE % (player.name, event)
            em.add_field(
                name="",
                value=s.BAD_EVENT
                % (
                    self.bot.ctime(val),
                    player.level + 1,
                    self.bot.ctime(player.nextxp - player.currentxp),
                ),
            )
        elif event_choice[0] == "hog":  # Lucky
            val = int(int(10 + random.randint(1, 8)) / alvar * player.nextxp)
            player.nextxp -= val
            if player.nextxp - player.currentxp < 0:
                player.nextxp = player.currentxp + 1
            em.title = s.HOG_EVENT_TITLE % player.name
            em.add_field(
                name="",
                value=s.HOG_EVENT
                % (
                    self.bot.ctime(val),
                    player.level + 1,
                    self.bot.ctime(player.nextxp - player.currentxp),
                ),
            )
        else:
            print("Something went wrong choosing a random event")

        item = await get_item(player)
        item_embed = discord.Embed(color=discord.Color(cfg.COLOR_LOOT))
        item_embed.title = s.NEW_LOOT % player.name
        item_embed.add_field(name="", value=self.bot.item_string(item[0]), inline=False)
        item_embed.set_footer(
            text=s.UPGRADE % item[1] if item[2] else s.NO_UPGRADE % item[1]
        )
        if self.bot.channel:
            if player.optin:
                await self.bot.channel.send(
                    f"<@!{player.uid}>", embeds=[em, item_embed]
                )
            else:
                await self.bot.channel.send(embeds=[em, item_embed])


async def setup(bot):
    """Cog setup"""
    await bot.add_cog(Events(bot))
