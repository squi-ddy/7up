from typing import Dict, List, Optional, Tuple

import asyncpg
from pydantic.dataclasses import dataclass

from utils.env import Settings


@dataclass(frozen=True)
class GameRecord:
    guild: int
    channel: int
    game_type: int = 0
    current_count: int = 1
    last_user: Optional[int] = None


@dataclass
class GameRecordWrapper:
    record: Optional[GameRecord] = None
    updated: bool = False


class GameDatabase:
    _settings: Settings
    _records: Dict[int, GameRecordWrapper]

    def __init__(self, settings: Settings):
        self._settings = settings
        self._records = {}

    async def _get_conn(self) -> asyncpg.Connection:
        conn: asyncpg.Connection = await asyncpg.connect(  # type: ignore
            host=self._settings.db_host,
            user=self._settings.db_user,
            port=self._settings.db_port,
            password=self._settings.db_pass,
            database=self._settings.db_name,
        )

        return conn

    async def get_record(self, guild: int) -> Optional[GameRecord]:
        if guild in self._records:
            return self._records[guild].record

        # Retrieve from database
        conn: asyncpg.Connection = await self._get_conn()
        record = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", guild)
        await conn.close()

        game_record: Optional[GameRecord] = GameRecord(**record) if record else None

        self._records[guild] = GameRecordWrapper(record=game_record)

        return game_record

    async def set_record(self, record: GameRecord) -> None:
        guild = record.guild

        if guild in self._records:
            self._records[guild].record = record
            self._records[guild].updated = True

        self._records[guild] = GameRecordWrapper(record=record, updated=True)

    async def save_records(self) -> None:
        to_update: List[Tuple] = []
        for record_wrapper in self._records.values():
            record = record_wrapper.record

            if record_wrapper.updated and record is not None:
                to_update.append(
                    (
                        record.guild,
                        record.channel,
                        record.game_type,
                        record.current_count,
                        record.last_user,
                    )
                )

        conn: asyncpg.Connection = await self._get_conn()
        statement = await conn.prepare(
            "INSERT INTO data(guild, channel, game_type, current_count, last_user) "
            + "VALUES ($1, $2, $3, $4, $5) "
            + "ON CONFLICT (guild) DO UPDATE "
            + "SET channel=$2, game_type=$3, current_count=$4, last_user=$5"
        )

        await statement.executemany(to_update)
        await conn.close()
