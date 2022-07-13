import nextcord
from nextcord.ext import commands


class MiscCog(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot) -> None:
        super(MiscCog, self).__init__()

        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(activity=nextcord.Game(name=f"7up in {len(self.bot.guilds)} servers!"))

    @commands.Cog.listener()
    async def on_guild_join(self) -> None:
        await self.bot.change_presence(activity=nextcord.Game(name=f"7up in {len(self.bot.guilds)} servers!"))

    @commands.Cog.listener()
    async def on_guild_remove(self) -> None:
        await self.bot.change_presence(activity=nextcord.Game(name=f"7up in {len(self.bot.guilds)} servers!"))
