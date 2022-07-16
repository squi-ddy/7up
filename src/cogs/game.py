import asyncio
from datetime import datetime, timezone
from typing import List, Optional, Type

import nextcord
from nextcord.ext import commands, tasks

from games import CountingGame, GameSelector, ValidationResult
from games.util import process_ignores
from util import FooterType, GameDatabase, GameRecord, Paginator


class GameCog(commands.Cog):
    bot: commands.Bot
    database: GameDatabase
    lock: asyncio.Lock

    def __init__(self, bot: commands.Bot, database: GameDatabase):
        super(GameCog, self).__init__()

        self.bot = bot
        self.database = database
        self.lock = asyncio.Lock()
        self.save_data.start()

    def cog_unload(self) -> None:
        self.save_data.cancel()

    @nextcord.slash_command(name="ping", description="Pong!")
    async def ping(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.send_message(f"Pong! Latency is {round(self.bot.latency * 1000)}ms!", ephemeral=True)

    @nextcord.slash_command(
        name="bind",
        description="Bind 7up to a text channel.",
        dm_permission=False,
        default_member_permissions=nextcord.Permissions(manage_channels=True),
    )
    async def bind(
        self,
        interaction: nextcord.Interaction,
        *,
        channel: nextcord.abc.GuildChannel,
    ) -> None:
        if not interaction.guild:
            return

        async with self.lock:
            record: Optional[GameRecord] = await self.database.get_record(interaction.guild.id)

            if not record:
                await self.database.set_record(GameRecord(guild=interaction.guild.id, channel=channel.id))
                return

            record.channel = channel.id
            record.reset_game()

        await interaction.response.send_message(f"Successfully bound to {channel.mention}!")

    @nextcord.slash_command(name="help", description="Information about 7up and its games")
    async def help(self, interaction: nextcord.Interaction) -> None:
        if interaction.user is None:
            return

        seven_up_help = nextcord.Embed(
            title="Hi! I'm 7up!",
            description="I love counting games like **7up** and **FizzBuzz**!\n"
            + "Click through the pages to see what games I have on offer!\n"
            + "I've sorted them in difficulty order, so pick what you like best!\n"
            + "Bind me to a channel with `/bind`, and pick a game with `/game`!\n\n"
            + "By the way, use backticks (`) to quote numbers, and I'll ignore them.",
        )

        paginator_pages: List[nextcord.Embed] = [seven_up_help]

        game_type = -1

        if interaction.guild is not None:
            async with self.lock:
                record: Optional[GameRecord] = await self.database.get_record(interaction.guild.id)

            game_type = 0
            if record is not None:
                game_type = record.game_type

        for i, game in enumerate(GameSelector.games):
            embed: nextcord.Embed = game.get_embed()

            if i == game_type and embed.description != nextcord.Embed.Empty:
                embed.description += "\n\n***This game is currently selected!***"  # type: ignore

            paginator_pages.append(embed)

        message = await interaction.response.send_message(embed=paginator_pages[0], ephemeral=True)

        paginator = Paginator(
            message=message,
            embeds=paginator_pages,
            author=interaction.user,
            bot=self.bot,
            embed_footer_type=FooterType.PAGE_NUMBER,
            embed_footer_bot_icon=True,
        )

        await paginator.start()

    @nextcord.slash_command(
        name="game",
        description="Choose the game you want to play!",
        dm_permission=False,
        default_member_permissions=nextcord.Permissions(manage_channels=True),
    )
    async def choose_game(
        self,
        interaction: nextcord.Interaction,
        *,
        game_name: str = nextcord.SlashOption(choices=[game.get_title() for game in GameSelector.games]),
    ) -> None:
        if interaction.guild is None or interaction.channel is None:
            return

        game: Type[CountingGame] = GameSelector.get_game_by_name(game_name)

        async with self.lock:
            record: Optional[GameRecord] = await self.database.get_record(interaction.guild.id)

            if record is None:
                await interaction.response.send_message("Bind me to a channel first, silly!", ephemeral=True)
                return

            if record.channel != interaction.channel.id:
                await interaction.response.send_message("Talk to me in my bound channel, please.", ephemeral=True)
                return

            record.game_type = GameSelector.get_id_by_game(game)
            record.reset_game()

        await interaction.response.send_message(f"Success! You're now playing {game_name}!")

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message) -> None:
        if message.author.bot or not message.guild:
            return

        if (datetime.now(timezone.utc) - message.created_at).total_seconds() > 60:
            return

        success = True

        async with self.lock:
            record: Optional[GameRecord] = await self.database.get_record(message.guild.id)

            if record is None or message.channel.id != record.channel:
                return

            game: Type[CountingGame] = GameSelector.get_game_by_id(record.game_type)

            # PyCharm doesn't understand `message.clean_content`
            # noinspection PyTypeChecker
            validation: ValidationResult = game.is_valid(process_ignores(message.clean_content), record.current_count)

            if validation == ValidationResult.UNRELATED:
                return

            if validation == ValidationResult.REJECT or record.last_user == message.author.id:
                record.reset_game()
                success = False

            else:
                record.current_count += 1
                record.last_user = message.author.id

        if success:
            await message.add_reaction("✅")
        else:
            await message.add_reaction("❌")

            # noinspection PyTypeChecker
            clean_content = nextcord.utils.escape_markdown(message.clean_content)

            await message.reply(
                embed=nextcord.Embed(
                    colour=nextcord.Colour.dark_red(),
                    title="Loser!",
                    description=f"{message.author.mention} lost the game at {record.current_count}!",
                ).add_field(
                    name="Error Diagnosis:",
                    value=(
                        f"Should have said `{game.get_solution(record.current_count)}`, instead said "
                        f"`{clean_content}` "
                    )
                    if validation == ValidationResult.REJECT
                    else "Should have waited their turn",
                ),
                mention_author=True,
            )

    @tasks.loop(minutes=2.0)
    async def save_data(self) -> None:
        await self.database.save_records()

    @save_data.after_loop
    async def after_save_data(self) -> None:
        await self.database.save_records()
