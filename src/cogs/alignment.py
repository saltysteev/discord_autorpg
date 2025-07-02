"""
alignment.py
"""

import discord
from discord import app_commands
from discord.ext import commands

from bot import AutoBot
from utils.db import Player


class Align(discord.ui.View):
    def __init__(self):
        self.choice = 0
        super().__init__()

    @discord.ui.button(label="Good", style=discord.ButtonStyle.green)
    async def good(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Fires if player selects good"""
        self.choice = 1
        self.stop()

    @discord.ui.button(label="Neutral", style=discord.ButtonStyle.gray)
    async def neutral(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """Fires if player selects neutral"""
        self.choice = 0
        self.stop()

    @discord.ui.button(label="Evil", style=discord.ButtonStyle.red)
    async def evil(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Fires if player selects evil"""
        self.choice = 2
        self.stop()


class Alignment(commands.Cog):
    """Handler of alignment"""

    def __init__(self, bot: AutoBot):
        super().__init__()
        self.bot = bot

    @app_commands.command()
    async def align(self, ctx: discord.Interaction):
        """Sets your alignment to either good or evil"""
        view = Align()
        player = await Player.objects.get(uid=ctx.user.id)
        await ctx.response.send_message(
            "Select your desired alignment. This affects combat and events.",
            view=view,
            ephemeral=True,
        )
        await view.wait()
        match view.choice:
            case 1:
                align = "good"
            case 2:
                align = "evil"
            case _:
                align = "neutral"
        response_string = (
            f"You are already considered {align}."
            if player.align == view.choice
            else f"You are now considered {align}!"
        )
        if player.align != view.choice:
            player.align = view.choice
            await player.update(_columns=["align"])
        await ctx.edit_original_response(content=response_string, view=None)


async def setup(bot):
    """Cog setup"""
    await bot.add_cog(Alignment(bot))
