import os
from typing import Generator

import pytest
import sqlalchemy_utils
from playhouse.postgres_ext import PostgresqlExtDatabase

from shortcake.database.management import ShortcakeDatabase

DATABASE_HOSTNAME = os.environ.get("POSTGRES_HOSTNAME", "postgres")
DATABASE_NAME = "shortcake_test"


@pytest.fixture(autouse=True)
def postgres_test_db() -> Generator[PostgresqlExtDatabase, None, None]:
    database = ShortcakeDatabase(
        database_name=DATABASE_NAME,
        hostname=DATABASE_HOSTNAME,
    )

    database.create(overwrite=True)
    database.connect()
    database.create_tables()

    yield database.database

    database.drop_tables()
    database.database.close()

    sqlalchemy_utils.drop_database(database.uri)
