from typing import Generator, Type, TypeVar

T = TypeVar("T")


def all_subclasses(
    cls: Type[T], ignore_private: bool = True
) -> Generator[Type[T], None, None]:
    """Get all subclasses of cls, recursively.

    If ignore_private is True, classes with names that start with '_' are ignored.
    """
    for subclass in cls.__subclasses__():
        yield from all_subclasses(subclass)

        # Ignore private classes
        if subclass.__name__.startswith("_") and ignore_private:
            continue

        yield subclass
