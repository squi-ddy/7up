from typing import Optional

import asyncpg

from utils.env import Settings


class Database:
    _pool: Optional[asyncpg.Pool] = None
    _settings: Settings

    def __init__(self, settings: Settings):
        self._settings = settings

    async def get_pool(self) -> asyncpg.Pool:
        if self._pool is not None:
            return self._pool

        self._pool = await asyncpg.create_pool(
            host=self._settings.db_host,
            user=self._settings.db_user,
            port=self._settings.db_port,
            password=self._settings.db_pass,
            database=self._settings.db_name
        )
        return self._pool
