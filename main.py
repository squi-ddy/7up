import logging

import discord
import uvloop

from cogs import Game
from utils import GameDatabase, loaded_settings


def main():
    logging.basicConfig(level=logging.INFO)

    uvloop.install()

    database = GameDatabase(loaded_settings)

    intents = discord.Intents.default()
    intents.message_content = True

    bot = discord.Bot(intents=intents, debug_guilds=[789468266803625984])

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game(name="7up"))

    bot.add_cog(Game(bot, database))

    bot.run(loaded_settings.bot_token)


if __name__ == "__main__":
    main()
