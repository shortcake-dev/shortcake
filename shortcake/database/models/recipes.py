import uuid
from typing import List

from peewee import CompositeKey, ForeignKeyField, IntegerField, TextField, UUIDField

from .base import BaseModel
from .ingredients import Ingredient


class Recipe(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = TextField()
    description = TextField()

    @property
    def ingredients(self) -> List[Ingredient]:
        return (
            Ingredient.select()
            .join(RecipeIngredient)
            .where(RecipeIngredient.recipe == self)
        )


class RecipeIngredient(BaseModel):
    recipe = ForeignKeyField(Recipe)
    ingredient = ForeignKeyField(Ingredient)

    measurement = TextField()
    modifier = TextField(null=True)

    class Meta:
        primary_key = CompositeKey("recipe", "ingredient")


class RecipeStep(BaseModel):
    recipe = ForeignKeyField(Recipe)
    step_index = IntegerField()

    text = TextField()

    class Meta:
        primary_key = CompositeKey("recipe", "step_index")
