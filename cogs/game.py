from typing import Optional

import asyncpg
import discord
from asyncpg import Record
from discord.ext import commands

from games import CountingGame, GameSelector
from games.base import ValidationResult
from utils import Database


class Game(commands.Cog):
    database: Database

    def __init__(self, bot: discord.Bot, database: Database):
        self.bot = bot
        self.database = database

    @commands.slash_command(name="ping", description="Pong!")
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        await ctx.respond(f"Pong! Latency is {round(self.bot.latency * 1000)}ms!")

    @commands.slash_command(name="bind", description="Bind 7up to a text channel.")
    async def bind(self, ctx: discord.ApplicationContext, *,
                   channel: Optional[discord.TextChannel] = None) -> None:
        channel = channel or ctx.channel

        conn: asyncpg.Connection
        async with (await self.database.get_pool()).acquire() as conn:
            async with conn.transaction():
                result: Optional[Record] = (
                    await conn.fetchrow("SELECT channel FROM data WHERE guild=$1", ctx.guild_id)
                )

                curr_channel = 0
                if result is not None:
                    curr_channel = result['channel']

                if curr_channel == channel.id:
                    await ctx.respond(f"Already bound to {channel.mention}!")
                    return

                await conn.execute(
                    """
                        INSERT INTO data(guild, channel, last_user, current_count) 
                        VALUES ($1, $2, NULL, 1) 
                        ON CONFLICT (guild) DO UPDATE 
                        SET channel=$2, last_user=NULL, current_count=1
                    """,
                    ctx.guild_id, channel.id)

        await ctx.respond(f"Successfully bound to {channel.mention}!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        conn: asyncpg.Connection
        async with (await self.database.get_pool()).acquire() as conn:
            async with conn.transaction():
                result: Optional[Record] = (
                    await conn.fetchrow(
                        """
                            SELECT game_type, current_count, last_user 
                            FROM data 
                            WHERE channel=$1 AND guild=$2
                        """,
                        message.channel.id, message.guild.id)
                )

                if result is None:
                    return

                game: CountingGame = GameSelector.get_game_by_id(result['game_type'])

                validation: ValidationResult = game.is_valid(message.content, result['current_count'])

                if validation == ValidationResult.UNRELATED:
                    return

                if validation == ValidationResult.REJECT or result['last_user'] != message.author.id:
                    await message.add_reaction("❌")
                    await conn.execute(
                        """
                            UPDATE data 
                            SET current_count=1, last_user=NULL 
                            WHERE channel=$1 AND guild=$2
                        """,
                        message.channel.id, message.guild.id)

                else:
                    await message.add_reaction("✅")
                    await conn.execute(
                        """
                            UPDATE data 
                            SET current_count=current_count+1, last_user=$3 
                            WHERE channel=$1 AND guild=$2
                        """,
                        message.channel.id, message.guild.id, message.author.id)
