from collections import Generator

from . import ingredients, recipes
from .base import BaseModel, database_proxy


def _all_subclasses(cls: type) -> Generator[type, None, None]:
    """Get all subclasses of cls, recursively. Classes with names that start
    with '_' are ignored."""
    for subclass in cls.__subclasses__():
        yield from _all_subclasses(subclass)
        # Ignore private classes
        if not subclass.__name__.startswith("_"):
            yield subclass


all_models = set(_all_subclasses(BaseModel))
