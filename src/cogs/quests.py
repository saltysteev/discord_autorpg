"""
quests.py
"""

import random
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

import utils.config as cfg
from utils.db import Player, Quest

from bot import AutoBot


class Quests(commands.Cog):
    """Handler of quests"""

    def __init__(self, bot: AutoBot):
        super().__init__()
        self.bot = bot

    @staticmethod
    def return_questers(lst: list) -> str:
        return ", ".join(lst[:-1]) + f" and {lst[-1]}"

    async def startquest(self):
        goal = random.choice(self.bot.readfile("quests"))
        questers = []  # List of player names for the embed / quest description
        quester_pings = []  # List of player IDs in Discord ping format <@!>
        quester_ids = []  # List of player IDs for SQL statement
        eligible = await Player.objects.all(online=True, level__gte=20)
        if not eligible or len(eligible) < 2:
            return
        players = random.choices(eligible, k=random.randint(2, 4))
        endxp = len(players) * random.choice([36000, 39600, 43200])
        qid = int(datetime.today().timestamp())
        for i in players:
            if i.optin:
                quester_pings.append(f"<@!{i.uid}>")
            questers.append(i.name)
            quester_ids.append(i.uid)
            i.onquest = True
            i.qid = qid
        await Player.objects.bulk_update(players, columns=["onquest", "qid"])
        await Quest.objects.create(
            qid=qid,
            players=self.return_questers(questers),
            goal=goal,
            endxp=endxp,
            currentxp=0,
            deadline=qid + 86400,
        )
        embed = discord.Embed(
            color=discord.Color(cfg.COLOR_QUEST),
            title=":park: A new quest has been placed on the notice board!",
        )
        embed.add_field(
            name="",
            value=f"{self.return_questers(questers)} have been graciously chosen by the sentient Beings to {goal}.\nThey have **24 hours** to complete their journey which will take **{self.bot.ctime(endxp)}** collectively.",
        )
        if self.bot.channel:
            await self.bot.channel.send(" ".join(quester_pings), embed=embed)

    async def endquest(self, quest: Quest, win):
        eligible = await Player.objects.all(online=True, level__gte=20)
        total = cfg.QUEST_REWARD if win else cfg.QUEST_PENALTY
        quester_pings = []
        for p in eligible:
            nextval = int(total * (p.nextxp - p.currentxp))
            p.nextxp = p.nextxp - nextval if win else p.nextxp + nextval
        await Player.objects.bulk_update(eligible, columns=["nextxp"])
        questers = await Player.objects.all(onquest=True)
        for i in questers:
            if i.optin:
                quester_pings.append(f"<@!{i.uid}>")
            i.onquest = False
            i.qid = 0
            i.totalquests += 1
        await Player.objects.bulk_update(
            questers, columns=["onquest", "qid", "totalquests"]
        )
        await Quest.objects.delete(qid=quest.qid)
        embed = discord.Embed(color=discord.Color(cfg.COLOR_QUEST))
        if win:
            embed.title = f":park: Rejoice! {quest.players} have reached their destinations **completing their quest!**"
            embed.add_field(
                name="",
                value="They spread their plunder throughout the realm, boosting everyone's clock **10% towards the next level!**",
            )
        elif not win:
            embed.title = f":park: {quest.players} have **failed in their quest** and bring down the wrath of Gods upon the realm!"
            embed.add_field(
                name="",
                value="They are displeased, slowing everyone's clock **5% towards the next level!**",
            )
        if self.bot.channel:
            await self.bot.channel.send(" ".join(quester_pings), embed=embed)

    @app_commands.command()
    async def quest(self, ctx: discord.Interaction):
        """Shows the current realm quest status"""
        quest = await Quest.objects.get_or_none()
        if not quest:
            await ctx.response.send_message(
                "```There currently are no adventurers in this guild on a quest.```"
            )
        else:
            embed = discord.Embed(color=discord.Color(cfg.COLOR_QUEST))
            embed.title = f":park: Quest status for {ctx.guild}"
            embed.add_field(
                name="",
                value=f"{quest.players} are on the blessed path to {quest.goal} and will reach their destination in **{self.bot.ctime(quest.endxp - quest.currentxp)}** collectively.\n"
                f"They have **{self.bot.ctime(quest.deadline - int(datetime.now().timestamp()))}** remaining to appease the gods.\n",
            )
            await ctx.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Quests(bot))
