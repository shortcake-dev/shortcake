import uuid

from peewee import CompositeKey, ForeignKeyField, IntegerField, TextField, UUIDField

from .base import BaseModel
from .ingredients import Ingredient


class Recipe(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = TextField()
    description = TextField()


class RecipeIngredient(BaseModel):
    recipe = ForeignKeyField(Recipe)
    ingredient = ForeignKeyField(Ingredient)
    measurement = TextField()

    class Meta:
        primary_key = CompositeKey("recipe", "ingredient")


class RecipeStep(BaseModel):
    recipe = ForeignKeyField(Recipe)
    step_index = IntegerField()

    text = TextField()

    class Meta:
        primary_key = CompositeKey("recipe", "step_index")
