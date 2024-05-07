"""
maps.py
"""

import random

import discord
from discord.ext import commands

from utils import config as cfg
from utils.db import Player

from bot import AutoBot


class Maps(commands.Cog):
    """Handler of maps"""

    def __init__(self, bot: AutoBot):
        super().__init__()
        self.bot = bot
        self.previous_bump = []

    async def mapmove(self, player: Player):
        """Player movement"""
        player.x = random.randint(player.x - 1, player.x + 1) % cfg.MAP_SIZE[0]
        player.y = random.randint(player.y - 1, player.y + 1) % cfg.MAP_SIZE[1]
        if cfg.ENABLE_COMBAT:
            opp = await Player.objects.exclude(uid=player.uid).get_or_none(
                x=player.x, y=player.y, online=True
            )
            if not opp:
                return
            if player.name and opp.name in self.previous_bump:
                return
            embed = discord.Embed(color=discord.Color(cfg.COLOR_COMBAT))
            embed.title = (
                ":crossed_swords: Two adventures encounter each other in the realm!"
            )
            if random.random() <= 0.25 and player.level >= 25:
                challenge = self.bot.get_cog("Challenge")
                cstring = await challenge.challenge_opp(player, opp)
            else:
                cstring = f"{player.name} and {opp.name} honorably bow to each other and pass, continuing on their journey peacefully."
            self.previous_bump = [player.name, opp.name]
            embed.add_field(name="", value=cstring)
            pings = []
            if player.optin:
                pings.append(f"<@!{player.uid}>")
            if opp.optin:
                pings.append(f"<@!{opp.uid}>")
            if self.bot.guild.system_channel:
                await self.bot.guild.system_channel.send(" ".join(pings), embed=embed)


async def setup(bot):
    """Cog setup"""
    await bot.add_cog(Maps(bot))
