from shortcake.database.models.ingredients import Ingredient as DBIngredient
from shortcake.database.models.recipes import Recipe as DBRecipe
from shortcake.database.models.recipes import RecipeIngredient as DBRecipeIngredient
from shortcake.database.models.recipes import RecipeStep as DBRecipeStep

from tests.utils import call_counter

from . import Ingredient as FakeIngredient


@call_counter
def Recipe(
    *, name: str = None, description: str = None, counter_index: int = None
) -> DBRecipe:
    recipe = DBRecipe.create(
        name=name or f"Ingredient {counter_index}",
        description=description or f"Description {counter_index}",
    )

    return recipe


@call_counter
def RecipeIngredient(
    *,
    recipe: DBRecipe = None,
    ingredient: DBIngredient = None,
    quantity: float = None,
    unit: str = None,
    counter_index: int = None,
) -> DBRecipeIngredient:
    recipe_ingredient = DBRecipeIngredient.create(
        recipe=recipe or Recipe(),
        ingredient=ingredient or FakeIngredient(),
        quantity=quantity if quantity is not None else counter_index,
        unit=unit if unit is not None else "unit",
    )

    return recipe_ingredient


@call_counter
def RecipeStep(
    *,
    recipe: DBRecipe = None,
    step_index: int = None,
    text: str = None,
    counter_index: int = None,
) -> DBRecipeStep:
    recipe_step = DBRecipeStep.create(
        recipe=recipe or Recipe(),
        step_index=step_index if step_index is not None else counter_index,
        text=text or f"Step {counter_index}",
    )

    return recipe_step
