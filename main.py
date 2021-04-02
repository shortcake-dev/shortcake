import sqlalchemy_utils
import uvicorn

from shortcake.asgi.app import BrainFrameApp
from shortcake.database.management import DBConfig, create_database, init_database

DATABASE_HOSTNAME = "postgres"
DATABASE_NAME = "shortcake"


def main():
    db_config = DBConfig(database=DATABASE_NAME, hostname=DATABASE_HOSTNAME)

    if not sqlalchemy_utils.database_exists(db_config.uri):
        create_database(db_config)

    init_database(db_config)

    app = BrainFrameApp(debug=True)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")


if __name__ == "__main__":
    main()
