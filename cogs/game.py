import asyncio
from typing import List, Optional, Type, Union

import discord
from discord.ext import commands, pages, tasks

from games import CountingGame, GameSelector
from games.base import ValidationResult
from utils import GameDatabase
from utils.db import GameRecord


class Game(commands.Cog):
    bot: discord.Bot
    database: GameDatabase
    lock: asyncio.Lock

    def __init__(self, bot: discord.Bot, database: GameDatabase):
        self.bot = bot
        self.database = database
        self.lock = asyncio.Lock()
        self.save_data.start()

    def cog_unload(self) -> None:
        self.save_data.cancel()

    @commands.slash_command(name="ping", description="Pong!")
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        await ctx.respond(f"Pong! Latency is {round(self.bot.latency * 1000)}ms!", ephemeral=True)

    @commands.slash_command(name="bind", description="Bind 7up to a text channel.")
    @discord.default_permissions(manage_channels=True)
    async def bind(
        self,
        ctx: discord.ApplicationContext,
        *,
        channel: Optional[discord.TextChannel] = None,
    ) -> None:
        channel = channel or ctx.channel

        async with self.lock:
            await self.database.set_record(GameRecord(guild=ctx.guild.id, channel=channel.id))

        await ctx.respond(f"Successfully bound to {channel.mention}!")

    @commands.slash_command(name="help", description="Information about 7up and its games")
    async def help(self, ctx: discord.ApplicationContext):
        seven_up_help = discord.Embed(
            title="Hi! I'm 7up!",
            description="I love counting games like **7up** and **FizzBuzz**!\n"
            + "Click through the pages to see what games I have on offer!\n"
            + "I've sorted them in difficulty order, so pick what you like best!\n"
            + "Bind me to a channel with `/bind`, and pick a game with `/game`!",
        )

        paginator_pages: List[Union[List[discord.Embed], discord.Embed]] = [seven_up_help]

        for game in GameSelector.games:
            paginator_pages.append(game.get_embed())

        paginator = pages.Paginator(pages=paginator_pages)

        await paginator.respond(ctx.interaction, ephemeral=True)

    @commands.slash_command(name="game", description="Choose the game you want to play!")
    @discord.commands.option("game_name", choices=[game.get_title() for game in GameSelector.games])
    async def choose_game(
        self,
        ctx: discord.ApplicationContext,
        *,
        game_name: str,
    ) -> None:
        game: Type[CountingGame] = GameSelector.get_game_by_name(game_name)

        async with self.lock:
            record: Optional[GameRecord] = await self.database.get_record(ctx.guild.id)

            if record is None:
                await ctx.respond("Bind me to a channel first, silly!", ephemeral=True)
                return

            if record.channel != ctx.channel.id:
                await ctx.respond("Talk to me in my bound channel, please.", ephemeral=True)
                return

            await self.database.set_record(
                GameRecord(guild=ctx.guild.id, channel=record.channel, game_type=GameSelector.get_id_by_game(game))
            )

        await ctx.respond(f"Success! You're now playing {game_name}!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot or not message.guild:
            return

        async with self.lock:
            record: Optional[GameRecord] = await self.database.get_record(message.guild.id)

            if record is None or message.channel.id != record.channel:
                return

            game: Type[CountingGame] = GameSelector.get_game_by_id(record.game_type)

            validation: ValidationResult = game.is_valid(message.content, record.current_count)

            if validation == ValidationResult.UNRELATED:
                return

            if validation == ValidationResult.REJECT or record.last_user == message.author.id:
                await message.add_reaction("❌")

                await message.reply(
                    embed=discord.Embed(
                        colour=discord.Colour.dark_red(),
                        title="Loser!",
                        description=f"{message.author.mention} lost the game at {record.current_count}!",
                    ).add_field(
                        name="Error Diagnosis:",
                        value=(
                            f"Should have said `{game.get_solution(record.current_count)}`, instead said "
                            f"`{message.content}` "
                        )
                        if validation == ValidationResult.REJECT
                        else "Should have waited their turn",
                    ),
                    mention_author=True,
                )

                await self.database.set_record(
                    GameRecord(
                        guild=record.guild,
                        channel=record.channel,
                        game_type=record.game_type,
                    )
                )

            else:
                await message.add_reaction("✅")

                await self.database.set_record(
                    GameRecord(
                        guild=record.guild,
                        channel=record.channel,
                        game_type=record.game_type,
                        current_count=record.current_count + 1,
                        last_user=message.author.id,
                    )
                )

    @tasks.loop(minutes=2.0)
    async def save_data(self):
        await self.database.save_records()

    @save_data.after_loop
    async def after_save_data(self):
        await self.database.save_records()
