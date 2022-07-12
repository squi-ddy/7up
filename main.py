import logging

import nextcord
import uvloop
from nextcord.ext import commands

from cogs import GameCog
from utils import GameDatabase, loaded_settings


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    uvloop.install()

    database = GameDatabase(loaded_settings)

    intents = nextcord.Intents.default()
    # noinspection PyDunderSlots,PyUnresolvedReferences
    intents.message_content = True

    bot: commands.Bot = commands.Bot(intents=intents)  # type: ignore

    @bot.event
    async def on_ready() -> None:
        await bot.change_presence(activity=nextcord.Game(name="7up"))

    bot.add_cog(GameCog(bot, database))

    bot.run(loaded_settings.bot_token)


if __name__ == "__main__":
    main()
