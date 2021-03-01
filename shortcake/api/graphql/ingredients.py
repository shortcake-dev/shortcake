from __future__ import annotations

from typing import List

import strawberry

from shortcake.database.models.ingredients import Ingredient as DBIngredient


@strawberry.type
class Ingredient:
    id: strawberry.ID
    name: str

    @classmethod
    def get_ingredient(cls, id: strawberry.ID) -> Ingredient:
        # Note: id shadows a builtin until either of the following are solved:
        # https://github.com/strawberry-graphql/strawberry/issues/727
        # https://github.com/strawberry-graphql/strawberry/issues/725
        [db_ingredient] = DBIngredient.select().where(DBIngredient.id == id)

        return cls.from_db_model(db_ingredient)

    @classmethod
    def get_ingredients(cls) -> List[Ingredient]:
        db_ingredients = DBIngredient.select()

        return list(map(Ingredient.from_db_model, db_ingredients))

    @classmethod
    def from_db_model(cls, db_ingredient: DBIngredient) -> Ingredient:
        return Ingredient(id=db_ingredient.id, name=db_ingredient.name)
