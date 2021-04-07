# Run from project root
import json
import os
from pathlib import Path

from shortcake.database.management import ShortcakeDatabase
from shortcake.database.models.ingredients import Ingredient
from shortcake.database.models.recipes import Recipe, RecipeIngredient, RecipeStep

RECIPE_DIR = Path("resources", "recipes")
DATABASE_HOSTNAME = os.environ.get("POSTGRES_HOSTNAME", "postgres")
DATABASE_NAME = os.environ.get("POSTGRES_DATABASE", "shortcake")


def main():
    database = ShortcakeDatabase(
        database_name=DATABASE_NAME,
        hostname=DATABASE_HOSTNAME,
    )
    database.connect()

    for recipe_path in RECIPE_DIR.iterdir():
        recipe_json = json.loads(recipe_path.read_text())

        with database.database.atomic():
            create_recipe(recipe_json)


def create_recipe(recipe_json: dict) -> Recipe:

    recipe = Recipe.create(
        name=recipe_json["name"],
        description=recipe_json["description"],
    )

    for ingredient_json in recipe_json["ingredients"]:
        create_recipe_ingredient(ingredient_json, recipe)

    for step_index, step_json in enumerate(recipe_json["steps"]):
        create_recipe_step(step_json, step_index, recipe)

    return recipe


def create_recipe_ingredient(ingredient_json: dict, recipe: Recipe) -> RecipeIngredient:
    ingredient = create_ingredient(ingredient_json["name"])

    recipe_ingredient = RecipeIngredient.create(
        recipe=recipe,
        ingredient=ingredient,
        measurement=ingredient_json["measurement"],
        modifier=ingredient_json["modifier"],
    )

    return recipe_ingredient


def create_recipe_step(step_str: str, step_index: int, recipe: Recipe) -> RecipeStep:
    recipe_step = RecipeStep.create(recipe=recipe, step_index=step_index, text=step_str)

    return recipe_step


def create_ingredient(ingredient_name: str) -> Ingredient:
    ingredient, _ = Ingredient.get_or_create(
        name=ingredient_name,
    )

    return ingredient


if __name__ == "__main__":
    main()
