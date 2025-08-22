"""
user.py
"""

import random
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

import utils.config as cfg
import utils.strings as s
from bot import AutoBot
from utils.db import Player
from utils.loot import get_item


class User(commands.Cog):
    """Handler of players"""

    def __init__(self, bot: AutoBot):
        super().__init__()
        self.bot = bot

    async def levelup(self, player: Player):
        player.nextxp = int(cfg.TIME_BASE * (cfg.TIME_EXP ** (player.level + 1)))
        player.currentxp = 0
        player.level += 1
        em = discord.Embed(
            title=s.LEVEL_UP % (player.name, player.job, player.level),
            color=discord.Color(cfg.COLOR_LEVELUP),
        )
        em.set_thumbnail(url=player.avatar_url)
        em.add_field(
            name="Next Level", value=self.bot.ctime(player.nextxp), inline=True
        )
        item = await get_item(player)
        em.add_field(
            name=s.NEW_LOOT % player.name,
            value=self.bot.item_string(item[0]),
            inline=False,
        )
        footer = s.UPGRADE % item[1] if item[2] else s.NO_UPGRADE % item[1]
        em.set_footer(text=footer)
        if cfg.ENABLE_COMBAT and player.level >= cfg.MIN_CHALLENGE_LEVEL:
            eligible = await Player.objects.exclude(uid=player.uid).all(
                level__gte=cfg.MIN_CHALLENGE_LEVEL, online=True
            )
            if eligible:
                challenge = self.bot.get_cog("Challenge")
                cstring = await challenge.challenge_opp(player, random.choice(eligible))
                em.add_field(name=s.CHALLENGE_TITLE, value=cstring, inline=False)
        if self.bot.channel:
            if player.optin:
                await self.bot.channel.send(f"<@!{player.uid}>", embed=em)
            else:
                await self.bot.channel.send(embed=em)

    @app_commands.command()
    @app_commands.describe(member="Which player's profile to display")
    async def profile(self, ctx: discord.Interaction, member: Optional[discord.Member]):
        """Displays a player's profile, or your own if no argument is given. Example: /profile @steev"""
        player = await Player.objects.get(uid=member.id if member else ctx.user.id)
        nextlevel = player.nextxp - player.currentxp
        if nextlevel < 1:
            nextlevel = 1
        match player.align:
            case 1:
                alignment = "Good"
            case 2:
                alignment = "Evil"
            case _:
                alignment = "Neutral"
        qstring = "not on a quest" if not player.onquest else "on a quest!"
        em = discord.Embed(color=discord.Color(2899536))
        em.title = f"{player.name}'s Adventure Profile"
        em.url = f"{cfg.GAME_URL}/profile.php?uid={player.uid}"
        em.set_thumbnail(url=player.avatar_url)
        em.add_field(name="Level", value=player.level)
        em.add_field(name="Class", value=player.job)
        em.add_field(name="Alignment", value=alignment)
        em.add_field(name="Tokens", value=player.tokens)
        em.add_field(
            name="Next Level",
            value=self.bot.ctime(nextlevel),
        )
        em.add_field(name="Total Idled", value=self.bot.ctime(player.totalxp))
        if cfg.ENABLE_COMBAT:
            em.add_field(name="Duels", value=f"{player.wins}W / {player.loss}L")
        equip_embed = discord.Embed(color=discord.Color(2899536), title="Equipment")
        equip_embed.description = "".join(
            [
                f"{cfg.E_WEAPON} {self.bot.item_string(player.weapon)}\n"
                if player.weapon
                else "",
                f"{cfg.E_SHIELD} {self.bot.item_string(player.shield)}\n"
                if player.shield
                else "",
                f"{cfg.E_HELMET} {self.bot.item_string(player.helmet)}\n"
                if player.helmet
                else "",
                f"{cfg.E_CHEST} {self.bot.item_string(player.chest)}\n"
                if player.chest
                else "",
                f"{cfg.E_GLOVES} {self.bot.item_string(player.gloves)}\n"
                if player.gloves
                else "",
                f"{cfg.E_BOOTS} {self.bot.item_string(player.boots)}\n"
                if player.boots
                else "",
                f"{cfg.E_RING} {self.bot.item_string(player.ring)}\n"
                if player.ring
                else "",
                f"{cfg.E_AMULET} {self.bot.item_string(player.amulet)}"
                if player.amulet
                else "",
            ]
        )
        em.set_footer(
            text=f"They are currently {'online' if player.online else 'offline'} and {qstring}"
        )
        await ctx.response.send_message(embeds=[em, equip_embed])

    @app_commands.command()
    @app_commands.describe(amount="How many loot tokens to use?")
    async def pull(self, ctx: discord.Interaction, amount: Optional[int] = 1):
        """Uses a loot token to get a random item. Can use be used up to 10 times at once."""
        player = await Player.objects.get(uid=ctx.user.id)
        if player.tokens < 1:
            await ctx.response.send_message(
                s.NO_TOKENS,
                ephemeral=True,
            )
            return
        if amount > player.tokens:
            await ctx.response.send_message(
                s.NOT_ENOUGH % player.tokens,
                ephemeral=True,
            )
            return
        if amount > 10:
            await ctx.response.send_message(
                s.MAX_LIMIT,
                ephemeral=True,
            )
            return
        embed = discord.Embed(
            title=f"{ctx.user.name} {s.CHEST_FOUND}",
            color=discord.Color(cfg.COLOR_LOOT),
        )
        embed.set_thumbnail(url=ctx.user.display_avatar.url)
        embed.description = ""
        for _ in range(amount):
            item = await get_item(player)
            embed.description += (
                f"{self.bot.item_string(item[0])}{cfg.E_UPGRADE if item[2] else ''}\n"
            )
        await ctx.response.send_message(embed=embed)
        player.tokens -= amount
        await player.update(_columns=["tokens"])


async def setup(bot):
    await bot.add_cog(User(bot))
