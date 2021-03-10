import uuid

from peewee import TextField, UUIDField

from .base import BaseModel


class Ingredient(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = TextField(unique=True)
