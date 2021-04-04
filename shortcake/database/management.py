from typing import Set, Type

import sqlalchemy
import sqlalchemy_utils
from playhouse import postgres_ext

from shortcake.util.types import all_subclasses

from .models import BaseModel, database_proxy


class ShortcakeDatabase:
    def __init__(
        self,
        database_name: str,
        hostname: str,
        port: int = 5432,
        username: str = "postgres",
        password: str = "postgres",
    ):
        self.database_name = database_name
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

        self.database = postgres_ext.PostgresqlExtDatabase(
            database=database_name,
            host=hostname,
            port=port,
            user=username,
            password=password,
        )

    @property
    def models(self) -> Set[Type[BaseModel]]:
        return set(all_subclasses(BaseModel))

    @property
    def exists(self) -> bool:
        return sqlalchemy_utils.database_exists(self.uri)

    @property
    def uri(self) -> str:
        return (
            f"postgresql://{self.username}:{self.password}"
            f"@{self.hostname}:{self.port}"
            f"/{self.database_name}"
        )

    def create(self, *, overwrite: bool = True) -> None:
        # It seems that you cannot connect to an engine for a database that does not
        # exist. We connect to the default postgres database so that we can then create
        # the database that we actually want
        postgres_db_uri = (
            f"postgresql://{self.username}:{self.password}"
            f"@{self.hostname}:{self.port}"
            f"/postgres"
        )
        engine = sqlalchemy.create_engine(postgres_db_uri)

        if overwrite and sqlalchemy_utils.database_exists(self.uri):
            sqlalchemy_utils.drop_database(self.uri)

        # For some reason this has a race condition with the debugger when it runs
        #     psycopg2.errors.ActiveSqlTransaction: CREATE DATABASE cannot run
        #     inside a transaction block
        # sqlalchemy_utils.create_database(self.uri)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute(f"create database {self.database_name}")

    def initialize(self) -> None:
        database_proxy.initialize(self.database)

        self.database.connect(reuse_if_open=True)
        self.database.create_tables(self.models, safe=True)
        self.database.commit()

    def drop_tables(self) -> None:
        self.database.drop_tables(self.models)
