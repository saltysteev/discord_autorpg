"""
jobs.py
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot import AutoBot
from utils.db import Player


class Jobs(commands.Cog):
    """Handler of jobs"""

    def __init__(self, bot: AutoBot):
        super().__init__()
        self.bot = bot

    @app_commands.command()
    @app_commands.rename(arg="class")
    @app_commands.describe(arg="Define your custom class")
    async def job(self, ctx: discord.Interaction, arg: str):
        """Sets your class, only usable after lvl 10"""
        player = await Player.objects.get(uid=ctx.user.id)
        if player.level < 10:
            await ctx.response.send_message(
                "You must be level 10 or higher to change your class.",
                ephemeral=True,
            )
            return
        if not arg:
            await ctx.response.send_message(
                "You cannot have an empty class. /job <class>.",
                ephemeral=True,
            )
            return
        if not all(x.isalpha() or x.isspace() for x in arg):
            await ctx.response.send_message(
                "Class names can only contain letters.", ephemeral=True
            )
            return

        player.job = arg
        await player.update(_columns=["job"])
        await ctx.response.send_message(
            f"Your class has been changed to {arg}", ephemeral=True
        )


async def setup(bot):
    """Cog setup"""
    await bot.add_cog(Jobs(bot))
