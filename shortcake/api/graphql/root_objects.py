from typing import List

import strawberry

from .ingredients import Ingredient
from .recipes import Recipe


@strawberry.type
class Query:
    recipe: Recipe = strawberry.field(resolver=Recipe.get_recipe)
    recipes: List[Recipe] = strawberry.field(resolver=Recipe.get_recipes)

    ingredient: Ingredient = strawberry.field(resolver=Ingredient.get_ingredient)


schema = strawberry.Schema(query=Query)
