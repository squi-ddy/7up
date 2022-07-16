from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import asyncpg

from util.env import Settings, loaded_settings


@dataclass(kw_only=True)
class GameRecord:
    guild: int
    channel: int
    game_type: int = 0
    current_count: int = 1
    last_user: Optional[int] = None

    def __setattr__(self, key: str, value: Any) -> None:
        self.on_change()
        super(GameRecord, self).__setattr__(key, value)

    def reset_game(self) -> None:
        self.current_count = 1
        self.last_user = None

    # To be "overridden"
    def on_change(self) -> None:
        pass


class GameRecordWrapper:
    _record: GameRecord
    updated: bool = False

    def __init__(self, record: GameRecord, updated: bool = False):
        self._record = record
        self.updated = updated
        self._record.on_change = self._on_record_change  # type: ignore

    def _on_record_change(self) -> None:
        self.updated = True

    @property
    def record(self) -> GameRecord:
        return self._record

    @record.setter
    def record(self, value: GameRecord) -> None:
        self.updated = True
        self._record = value
        self._record.on_change = self._on_record_change  # type: ignore


class GameDatabase:
    _settings: Settings
    _records: Dict[int, GameRecordWrapper]

    def __init__(self, settings: Settings = loaded_settings):
        self._settings = settings
        self._records = {}

    async def _get_conn(self) -> asyncpg.Connection[Any]:
        conn: asyncpg.Connection[Any] = await asyncpg.connect(  # type: ignore
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
        conn: asyncpg.Connection[Any] = await self._get_conn()
        record = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", guild)
        await conn.close()

        if record is None:
            return None

        game_record: GameRecord = GameRecord(**record)

        self._records[guild] = GameRecordWrapper(record=game_record)

        return game_record

    async def set_record(self, record: GameRecord) -> None:
        guild = record.guild

        if guild in self._records:
            self._records[guild].record = record
            return

        self._records[guild] = GameRecordWrapper(record=record, updated=True)

    async def save_records(self) -> None:
        to_update: List[Tuple[Any, ...]] = []
        for record_wrapper in self._records.values():
            record = record_wrapper.record

            if record_wrapper.updated:
                to_update.append(
                    (
                        record.guild,
                        record.channel,
                        record.game_type,
                        record.current_count,
                        record.last_user,
                    )
                )

        conn: asyncpg.Connection[Any] = await self._get_conn()
        statement = await conn.prepare(
            "INSERT INTO data(guild, channel, game_type, current_count, last_user) "
            + "VALUES ($1, $2, $3, $4, $5) "
            + "ON CONFLICT (guild) DO UPDATE "
            + "SET channel=$2, game_type=$3, current_count=$4, last_user=$5"
        )

        await statement.executemany(to_update)
        await conn.close()
