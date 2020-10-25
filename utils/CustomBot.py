import asyncio

import aiohttp
import asyncpg
import discord

from discord.ext import commands

import datetime

from . import utils


async def get_prefix(bot: commands.AutoShardedBot, message: discord.Message):
    """If you're using a custom prefix you may want to override this."""

    return commands.when_mentioned_or("!")(bot, message)


class MyBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(get_prefix, *args, **kwargs)

        self.start_time = datetime.datetime.now()
        self.disabled_commands = {}

        self.loop = asyncio.get_event_loop()
        self.pool = self.loop.run_until_complete(
            asyncpg.create_pool(**utils.config("POSTGRES_INFO"))
        )
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        print(f"Currently in: {len(self.guilds)} guilds.")

    async def on_message(self, message: discord.Message):
        if not self.is_ready():
            return

        if (
            message.content == f"<@!{self.user.id}>"
            or message.content == f"<@{self.user.id}>"
        ):
            await message.channel.send(
                "Hey what's up? my prefixes are: "
                f"{', '.join((await get_prefix(self, message))[1:])}"
            )

        await self.process_commands(message)

    async def close(self):
        await super().close()
        await self.session.close()
        await self.pool.close()

    def get_uptime(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=int((datetime.datetime.now() - self.start_time).total_seconds()))
