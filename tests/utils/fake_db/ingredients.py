from shortcake.database import models

from tests.utils import call_counter


@call_counter
def Ingredient(*, name: str = None, counter_index: int = None):
    ingredient = models.ingredients.Ingredient.create(
        name=name or f"Ingredient {counter_index}",
    )

    return ingredient
