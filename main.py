import sqlalchemy_utils
import uvicorn
from starlette.applications import Starlette
from strawberry.asgi import GraphQL

from shortcake.api.graphql import schema
from shortcake.database.management import DBConfig, create_database, init_database

DATABASE_HOSTNAME = "postgres"
DATABASE_NAME = "shortcake"


def main():
    db_config = DBConfig(database=DATABASE_NAME, hostname=DATABASE_HOSTNAME)

    if not sqlalchemy_utils.database_exists(db_config.uri):
        create_database(db_config)

    init_database(db_config)

    app = Starlette(debug=True)
    graphql_app = GraphQL(schema, debug=True)

    path = "/"
    app.add_route(path, graphql_app)
    app.add_websocket_route(path, graphql_app)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")


if __name__ == "__main__":
    main()
