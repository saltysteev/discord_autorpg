"""
listeners.py
"""

import discord
from discord import app_commands
from discord.ext import commands

from utils.db import Player


class Listeners(commands.Cog):
    """Handler of generic commands"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def help(self, ctx: discord.Interaction):
        """Displays the list of commands available"""
        embed = discord.Embed(title="AutoRPG Command List")
        embed.add_field(name="/help", value="Shows the list of commands available")
        embed.add_field(
            name="/info", value="Shows version information and a link to the main page"
        )
        embed.add_field(
            name="/profile",
            value="Generates a link to view your stats. You can also look at another player's stats using /profile @name",
        )
        embed.add_field(
            name="/setclass <class>",
            value="After level 10 you can change your class. This is purely cosmetic and shows on your profile",
        )
        embed.add_field(
            name="/align",
            value="Allows you to choose Good, Evil, or stay Neutral. Check the Alignment section in the player handbook to see the differences",
        )
        embed.add_field(
            name="/quest",
            value="Shows the current quest information if there is one and it's participants",
        )
        embed.add_field(
            name="/raid",
            value="Lists the current raid. You can also view the current raid in the #raid channel if there is one.",
        )
        embed.add_field(
            name="/realm", value="Links to the current ongoing raid if there is one."
        )
        embed.add_field(
            name="/alert",
            value="Opt in or out to get mentioned if an event you're part of occurs.",
        )
        await ctx.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command()
    async def alert(self, ctx: discord.Interaction):
        """Opt in or out of getting mentioned after an event you're part of occurs"""
        player = await Player.objects.get(uid=ctx.user.id)
        player.optin = not player.optin
        await ctx.response.send_message(
            f"Your mentions are now set to {'ON' if player.optin else 'OFF'}",
            ephemeral=True,
        )
        await player.update(_columns=["optin"])


async def setup(bot):
    """Cog setup"""
    await bot.add_cog(Listeners(bot))
