import os

import pytest
import sqlalchemy_utils

from shortcake.database.management import (
    DBConfig,
    create_database,
    drop_tables,
    init_database,
)

DATABASE_HOSTNAME = os.environ.get("POSTGRES_HOSTNAME", "postgres")
DATABASE_NAME = "shortcake_test"


@pytest.fixture(autouse=True)
def postgres_test_db():
    db_config = DBConfig(database=DATABASE_NAME, hostname=DATABASE_HOSTNAME)

    create_database(db_config, overwrite=True)
    database = init_database(db_config)
    yield database

    drop_tables(database)
    database.close()
    del database

    sqlalchemy_utils.drop_database(db_config.uri)
