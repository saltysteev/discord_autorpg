"""
challenge.py
"""

import random
from typing import Optional

from discord.ext import commands

from utils.db import Player

from bot import AutoBot


weapon_slots = [
    "weapon",
    "shield",
    "helmet",
    "chest",
    "gloves",
    "boots",
    "ring",
    "amulet",
]


class Challenge(commands.Cog):
    """Handler of challenge"""

    def __init__(self, bot: AutoBot):
        super().__init__()
        self.bot = bot

    async def challenge_opp(self, player: Player, opp: Optional[Player] = None):
        """Called when a player duels another. Returns a string for embeds"""

        def get_dps(p) -> int:
            t = 0
            for i in p:
                if isinstance(i[1], dict):
                    t += i[1]["dps"]
            return t

        if not opp:
            eligible = await Player.objects.exclude(uid=player.uid).all(
                level__gte=25, online=True
            )
            opp = random.choice(eligible)
        player_max = int(get_dps(player) * (player.level / 100))
        opp_max = int(get_dps(opp) * (opp.level / 100))
        backstab_chance = random.random() <= 0.21 and player.align == 2
        match player.align:
            case 1:  # Good
                player_max += int((10 / 100) * player_max)
                alvar = 90
            case 2:  # Evil
                player_max -= int((10 / 100) * player_max)
                player_max = player_max * 2 if backstab_chance else player_max
                alvar = 110
            case _:
                alvar = 100
        nextval = int(
            (random.randint(3, 5) / alvar) * (player.nextxp - player.currentxp)
        )
        player_val = random.randint(1, player_max)
        opp_val = random.randint(1, opp_max)
        if player_val >= opp_val:
            swapped_slot: str = random.choice(weapon_slots)
            if all(
                [
                    player.align == 2,
                    random.random() < 0.15,
                    getattr(player, swapped_slot)["dps"]
                    > getattr(opp, swapped_slot)["dps"],
                ]
            ):
                temp = getattr(player, swapped_slot)
                setattr(player, swapped_slot, getattr(opp, swapped_slot))
                setattr(opp, swapped_slot, temp)
                cstring = (
                    f"{player.name} ({player_val}/{player_max}) has challenged {opp.name} ({opp_val}/{opp_max}) and was victorious in battle!\n"
                    f"Because of their evil nature, {player.name} swapped their {swapped_slot} with {opp.name}'s!\n"
                    f"Their time to next level has been accelerated by **{self.bot.ctime(nextval)}**!"
                )
                player.nextxp -= nextval
                player.wins += 1
            else:
                cstring = (
                    f"{player.name} ({player_val}/{player_max}) has challenged {opp.name} ({opp_val}/{opp_max}) and was victorious in battle!\n"
                    f"Their time to next level has been accelerated by **{self.bot.ctime(nextval)}**!"
                )
                player.nextxp -= nextval
                player.wins += 1
        else:
            cstring = (
                f"{player.name} ({player_val}/{player_max}) has challenged {opp.name} ({opp_val}/{opp_max}) and honorably lost in battle.\n"
                f"Their time to next level has been slowed by **{self.bot.ctime(nextval)}**."
            )
            player.nextxp += nextval
            player.totalxplost += nextval
            player.loss += 1
        if backstab_chance:
            cstring += f"\n{player.name} used **dirty tactics** during this fight and **backstabbed** {opp.name}!"
        return cstring


async def setup(bot):
    """Cog setup"""
    await bot.add_cog(Challenge(bot))
