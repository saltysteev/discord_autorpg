"""
loops.py
"""

import datetime
import random

import discord
from discord.ext import commands, tasks
from ormar.exceptions import NoMatch

from utils import config as cfg
from utils.db import Player, Quest


class Loops(commands.Cog):
    """Handler of main game loops"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.main_loop.start()
        self.hints.start()
        self.quest_check.start()

    async def cog_load(self):
        self.map_cog = self.bot.get_cog("Maps")
        self.event_cog = self.bot.get_cog("Events")
        self.mon_cog = self.bot.get_cog("Monsters")
        self.user_cog = self.bot.get_cog("User")
        self.quest_cog = self.bot.get_cog("Quests")

    @tasks.loop(seconds=cfg.INTERVAL)
    async def main_loop(self):
        """Loop timer that runs game logic on all online players"""
        players = await Player.objects.all(online=True)
        map_cog = self.bot.get_cog("Maps")
        for player in players:
            await map_cog.mapmove(player)
            if player.currentxp >= player.nextxp:
                await self.user_cog.levelup(player)
            player.lastlogin = int(datetime.datetime.today().timestamp())
            player.currentxp += cfg.INTERVAL
            player.totalxp += cfg.INTERVAL
        if random.randint(1, 4 * 86400) / cfg.INTERVAL < len(players):
            await self.event_cog.randomevent(random.choice(players))
        if random.randint(1, 8 * 86400) / cfg.INTERVAL < len(players):
            await self.mon_cog.encounter(random.choice(players))

        await Player.objects.bulk_update(
            players,
            columns=[
                "level",
                "nextxp",
                "totalxplost",
                "currentxp",
                "totalxp",
                "lastlogin",
                "wins",
                "loss",
                "x",
                "y",
            ],
        )

    @tasks.loop(minutes=cfg.INTERVAL)
    async def quest_check(self):
        """Loop timer that runs quest logic"""
        try:
            quest = await Quest.objects.get()
            count = (
                await Player.objects.filter(onquest=True, online=True).count()
                * cfg.INTERVAL
            )
            if datetime.datetime.today().timestamp() > quest.deadline:
                await self.quest_cog.endquest(quest, False)
            else:
                if quest.currentxp >= quest.endxp:
                    await self.quest_cog.endquest(quest, True)
                else:
                    quest.currentxp += count
                    await quest.update(_columns=["currentxp"])
        except NoMatch:
            if random.randint(1, 80000) < cfg.INTERVAL:
                if (
                    await Player.objects.filter(online=True).count() > 1
                ):  # Need at least 2 online players to start quest
                    await self.quest_cog.startquest()

    @tasks.loop(hours=12)
    async def hints(self):
        """Loop timer that sends a tip to the channel"""
        random_hint = random.choice(cfg.TIPS)
        embed = discord.Embed(title="")
        embed.add_field(name=":bulb: Did you know?", value=random_hint)
        await self.bot.talk_channel.send(embed=embed)

    @main_loop.before_loop
    async def before_main_loop(self):
        """Get cogs ready before background loop is started"""
        await self.bot.wait_until_ready()

    @hints.before_loop
    async def before_hints(self):
        """Function to run before hint timer is started"""
        await self.bot.wait_until_ready()


async def setup(bot):
    """Cog setup"""
    await bot.add_cog(Loops(bot))
