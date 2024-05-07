import logging
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils import config as cfg
from utils.db import Player, Quest
from utils.loot import get_item


class Admincomms(commands.Cog):
    """Handler of classes"""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @app_commands.command()
    @app_commands.default_permissions()
    async def reload(self, ctx: discord.Interaction, arg: str):
        """Reloads a cog"""
        if ctx.user.id not in cfg.SERVER_ADMINS:
            return
        try:
            await self.bot.reload_extension(arg)
            logging.info(f"Cog: {arg} reloaded")
        except commands.ExtensionError as e:
            await ctx.response.send_message(
                f"{e.__class__.__name__}: {e}", ephemeral=True
            )
        else:
            await ctx.response.send_message(
                f"Cog {arg} successfully reloaded", ephemeral=True
            )

    @app_commands.command()
    @app_commands.default_permissions()
    async def event(self, ctx: discord.Interaction, member: Optional[discord.Member]):
        """Spawns a random event"""
        if ctx.user.id not in cfg.SERVER_ADMINS:
            return
        player = await Player.objects.get_or_none(
            uid=member.id if member else ctx.user.id
        )
        if not player:
            await ctx.response.send_message("Player not found", ephemeral=True)
        else:
            event_cog = self.bot.get_cog("Events")
            await event_cog.randomevent(player)

    @app_commands.command()
    @app_commands.default_permissions()
    async def dropitem(
        self, ctx: discord.Interaction, member: Optional[discord.Member]
    ):
        """Spawns a new quest with random participants"""
        if ctx.user.id not in cfg.SERVER_ADMINS:
            return
        player = await Player.objects.get_or_none(
            uid=member.id if member else ctx.user.id
        )
        if not player:
            await ctx.response.send_message("Player not found", ephemeral=True)
        else:
            item = await get_item(player)
            await ctx.response.send_message(self.bot.item_string(item[0]))

    @app_commands.command()
    @app_commands.default_permissions()
    async def newquest(self, ctx: discord.Interaction):
        """Spawns a new quest with random participants"""
        if ctx.user.id not in cfg.SERVER_ADMINS:
            return
        quest = await Quest.objects.get_or_none()
        if quest:
            await ctx.response.send_message(
                "There's already an active quest", ephemeral=True
            )
        else:
            questcog = self.bot.get_cog("Quests")
            await questcog.startquest()

    @app_commands.command()
    @app_commands.default_permissions()
    async def endquest(self, ctx: discord.Interaction):
        """Ends the current quest if one is found"""
        if ctx.user.id not in cfg.SERVER_ADMINS:
            return
        quest = await Quest.objects.get_or_none()
        if not quest:
            await ctx.response.send_message("No quest active", ephemeral=True)
        else:
            questcog = self.bot.get_cog("Quests")
            await questcog.endquest(quest, True)

    @app_commands.command()
    @app_commands.default_permissions()
    async def fixusers(self, ctx: discord.Interaction):
        """Register a new user"""
        if ctx.user.id not in cfg.SERVER_ADMINS:
            return
        guild = ctx.guild
        if guild:
            for player in guild.members:
                await Player.objects.get_or_create(
                    uid=player.id,
                    _defaults={"name": player.display_name},
                )
            await ctx.response.send_message("Players registered", ephemeral=True)

    @app_commands.command()
    @app_commands.default_permissions()
    async def createroles(self, ctx: discord.Interaction):
        """Creates item rarity roles in the current guild"""
        if ctx.user.id not in cfg.SERVER_ADMINS:
            return
        await self.bot.createroles(ctx.guild)
        await ctx.response.send_message("Roles created", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Admincomms(bot))
