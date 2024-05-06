"""
bot.py
origin date: 12/31/2021

author: steev @ https://deadnet.org
special thanks through QA, testing, and security:
halfvoid, morrakiu, FixySLN, Welshnutter, Parzi, and many more

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import List

import discord
import uvloop
from discord.ext import commands

from utils import config as cfg
from utils.db import Player, database


class AutoBot(commands.Bot):
    """Main bot class"""

    def __init__(self, *args, initial_ext: List[str], **kwargs):
        intents = discord.Intents.all()
        super().__init__(*args, intents=intents, **kwargs)

        # configuration
        self.initial_ext = initial_ext
        self.pcount = 0

    async def setup_hook(self) -> None:
        logging.info("Starting bot - AutoRPG v%s", cfg.VERSION)

        # Load all the cogs from the cogs folder
        for ext in self.initial_ext:
            try:
                await self.load_extension(ext)
            except discord.DiscordException as exception:
                logging.error("Failed to load cog %s", ext, exc_info=exception)
        logging.info("Loaded %s cogs", len(self.initial_ext))

        # Sync slash commands to guild
        await self.tree.sync()

    async def on_ready(self):
        """Once setup_hook has finished and bot is ready"""
        self.game_channel = self.get_channel(cfg.GAME_CHANNEL)
        self.talk_channel = self.get_channel(cfg.TALK_CHANNEL)
        self.guild = self.get_guild(cfg.GUILD_ID)
        self.pcount = await Player.objects.filter(online=True).count()
        logging.info("Game started with %s online players", self.pcount)

    @staticmethod
    def ctime(seconds: int) -> str:
        """Takes a total seconds argument and makes it readable in time format."""
        intervals = (
            ("weeks", 604800),
            ("days", 86400),
            ("hours", 3600),
            ("minutes", 60),
            ("seconds", 1),
        )
        result = []
        for name, count in intervals:
            value = seconds // count
            seconds -= value * count
            if value:
                if value == 1:
                    name = name.rstrip("s")
                result.append(f"{value} {name}")
        return ", ".join(result)

    def item_string(self, item) -> str:
        if self.guild is None:
            pass

        item_role = discord.utils.get(self.guild.roles, name=item["rank"])
        return (
            f"<@&{item_role.id}> {item["quality"]} {item["prefix"]}{item["name"]}{item["suffix"]} ({item["condition"]}) ({item["dps"]})"
            if not item["flair"]
            else f"<@&{item_role.id}> {item["quality"]} {item["prefix"]}{item["name"]}{item["suffix"]} ({item["condition"]}) ({item["dps"]})\n> *{item["flair"]}*"
        )

    @staticmethod
    async def createroles(g: discord.Guild) -> None:
        """
        Check the current guild roles for item drops and make sure they're set to the correct colors.
        Call this if the roles ever get deleted or out of sync
        """
        rarity_roles = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Ascended"]
        color_codes = [0xFFFFFF, 0x2ECC71, 0x3498DB, 0x9B59B6, 0xE67E22, 0xFF1317]
        role_ids = []
        for name, color in zip(rarity_roles, color_codes):
            role = discord.utils.get(g.roles, name=name)
            if role is None:
                role = await g.create_role(name=name, colour=color)
            role_ids.append(role.id)

    @staticmethod
    def readfile(e: str) -> list[str]:
        """Read file function to get events and quests from the text files"""
        root_dir = Path(__file__).parent
        data_dir = (
            root_dir / "txtfiles" / cfg.HOLIDAY_LIST[cfg.HOLIDAY - 1]
            if cfg.HOLIDAY > 0
            else root_dir / "txtfiles"
        )
        file = (
            data_dir / f"{e}_{cfg.HOLIDAY_LIST[cfg.HOLIDAY - 1]}.txt"
            if cfg.HOLIDAY > 0
            else data_dir / f"{e}.txt"
        )
        with open(file, encoding="utf-8") as f:
            lines = [i.rstrip() for i in f]
            return lines

    async def on_message(self, _):
        pass

    async def on_member_join(self, ctx: discord.Member):
        """When a member joins the server, check if they exist and if not enter them into the database"""
        await Player.objects.get_or_create(
            uid=ctx.id,
            _defaults={"name": ctx.display_name},
        )

    async def on_member_remove(self, ctx: discord.Member):
        """When a member leaves the server, set them to offline, so they do not continue to gather experience"""
        await Player.objects.filter(uid=ctx.id).update(online=False)

    async def on_presence_update(self, _, after: discord.Member):
        """When a member goes offline, change their database status to offline"""
        online = after.status is not discord.Status.offline
        await Player.objects.filter(uid=after.id).update(online=online)

    async def on_member_update(self, _, after: discord.Member):
        """When a member changes their name or avatar, also change it in the database"""
        await Player.objects.filter(uid=after.id).update(
            name=after.display_name, avatar_url=after.display_avatar.url
        )


async def main():
    """Main bot launch function"""
    if not Path("src/utils/config.py").exists():
        return print("Config file missing or not changed!")

    token: str = cfg.DISCORD_TOKEN
    discord.utils.setup_logging(level=logging.INFO, root=True)
    exts = [
        "cogs.admincomms",
        "cogs.alignment",
        "cogs.challenge",
        "cogs.jobs",
        "cogs.events",
        "cogs.listeners",
        "cogs.loops",
        "cogs.maps",
        "cogs.monsters",
        "cogs.quests",
        "cogs.user",
    ]

    async with database:
        async with AutoBot(command_prefix="", initial_ext=exts) as bot:
            try:
                await bot.start(token)
            except discord.DiscordException as e:
                print(f"Bot failed to start: {e}")
            except KeyboardInterrupt:
                await database.disconnect()
                await bot.close()


if __name__ == "__main__":
    print(
        (
            " █████╗ ██╗   ██╗████████╗ ██████╗ ██████╗ ██████╗  ██████╗ \n"
            "██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝ \n"
            "███████║██║   ██║   ██║   ██║   ██║██████╔╝██████╔╝██║  ███╗\n"
            "██╔══██║██║   ██║   ██║   ██║   ██║██╔══██╗██╔═══╝ ██║   ██║\n"
            "██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║  ██║██║     ╚██████╔╝\n"
            "╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝      ╚═════╝ \n"
            "                                  ~ a discord game | @steev   "
        )
    )
    try:
        uvloop.run(main())
    except KeyboardInterrupt:
        pass
