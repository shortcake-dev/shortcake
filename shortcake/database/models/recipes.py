from __future__ import annotations

import uuid
from typing import Sequence

from peewee import CompositeKey, ForeignKeyField, IntegerField, TextField, UUIDField
from playhouse.hybrid import hybrid_property

from .base import BaseModel
from .ingredients import Ingredient


class Recipe(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = TextField()
    description = TextField()

    @hybrid_property
    def ingredients(self) -> Sequence[Ingredient]:
        ingredients = (
            Ingredient.select()
            .join(RecipeIngredient)
            .where(RecipeIngredient.recipe == self)
        )

        return ingredients

    @hybrid_property
    def steps(self) -> Sequence[RecipeStep]:
        steps = RecipeStep.select().where(RecipeStep.recipe == self)

        return steps


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
