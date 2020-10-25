import utils
import os
import discord
import logging
logging.basicConfig(level=logging.INFO)


os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

allowed_mentions = discord.AllowedMentions(
    everyone=False,
    roles=False,
    users=True
)

intents = discord.Intents.default()
intents.members = True

bot = utils.MyBot(
    status=discord.Status.dnd,
    activity=discord.Game("Connecting..."),
    allowed_mentions=allowed_mentions,
    chunk_guilds_at_startup=False,
    intents=intents,
    description=utils.config("BOT_DESCRIPTION")
)
bot.owner_ids = utils.config("BOT_OWNERS")
bot.colours = utils.config("COLOURS")
bot.exts = utils.config("HOT_RELOAD_EXTS")

for ext in bot.exts:
    bot.load_extension(ext)
    logging.info(f"Loaded {ext}")


async def secondary_on_ready():
    await bot.wait_until_ready()
    await bot.change_presence(
        activity=discord.Game("👀"),
        status=discord.Status.online
    )

bot.loop.create_task(secondary_on_ready())
bot.run(utils.config("TOKEN"))
