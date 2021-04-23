from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, WebSocketRoute
from strawberry.asgi import GraphQL

from shortcake.api.graphql import schema as graphql_schema


class ShortcakeApp(Starlette):
    def __init__(self, debug: bool = False):
        self.graphql_app = GraphQL(graphql_schema, debug=debug)

        routes = [
            Route("/", self.graphql_app),
            WebSocketRoute("/", self.graphql_app),
        ]

        middleware = []
        if debug:
            cors_middleware = Middleware(
                CORSMiddleware,
                allow_origin_regex=r"http://localhost:.*",
                allow_methods=["GET", "POST"],
            )
            middleware.append(cors_middleware)

        super().__init__(routes=routes, middleware=middleware, debug=debug)
