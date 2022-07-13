import pytest
import regex

from utils import GameDatabase, GameRecord

optional_extractor = regex.compile(r"Optional\[(.+)]")
map_python_to_postgres = {"int": ["bigint", "integer"]}


@pytest.mark.asyncio
async def test_db_columns():
    # Check whether the database defined in the .env is valid for the caching database

    database = GameDatabase()

    conn = await database._get_conn()
    column_info = await conn.fetch(
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='data'"
    )

    record_fields = GameRecord.__annotations__

    for column_name, data_type in column_info:
        assert column_name in record_fields

        python_data_type = record_fields.get(column_name)
        if match := optional_extractor.match(python_data_type):
            python_data_type = match.group(1)

        assert data_type in map_python_to_postgres[python_data_type]
