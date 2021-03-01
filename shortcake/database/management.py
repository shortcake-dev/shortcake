from dataclasses import dataclass

import sqlalchemy
import sqlalchemy_utils
from peewee import Database
from playhouse import postgres_ext

from .models import all_models
from .models.base import database_proxy


@dataclass
class DBConfig:
    database: str
    hostname: str
    port: int = 5432
    username: str = "postgres"
    password: str = "postgres"

    @property
    def uri(self) -> str:
        return (
            f"postgresql://{self.username}:{self.password}"
            f"@{self.hostname}:{self.port}"
            f"/{self.database}"
        )


def create_database(db_config: DBConfig, *, overwrite: bool = True) -> None:
    # It seems that you cannot connect to an engine for a database that does not
    # exist, so we connect to the default postgres database, so that we can then
    # create the database that we actually want
    postgres_db_uri = (
        f"postgresql://{db_config.username}:{db_config.password}"
        f"@{db_config.hostname}:{db_config.port}"
        f"/postgres"
    )
    engine = sqlalchemy.create_engine(postgres_db_uri)

    if overwrite and sqlalchemy_utils.database_exists(db_config.uri):
        sqlalchemy_utils.drop_database(db_config.uri)

    # For some reason this has a race condition with the debugger when it runs
    #     psycopg2.errors.ActiveSqlTransaction: CREATE DATABASE cannot run
    #     inside a transaction block
    # sqlalchemy_utils.create_database(db_config.uri)
    conn = engine.connect()
    conn.execute("commit")
    conn.execute(f"create database {db_config.database}")


def init_database(db_config: DBConfig) -> Database:
    database = postgres_ext.PostgresqlExtDatabase(
        database=db_config.database,
        host=db_config.hostname,
        port=db_config.port,
        user=db_config.username,
        password=db_config.password,
    )

    database_proxy.initialize(database)

    database.connect(reuse_if_open=True)
    database.create_tables(all_models, safe=True)
    database.commit()

    return database


def drop_tables(database: Database) -> None:
    database.drop_tables(all_models)
