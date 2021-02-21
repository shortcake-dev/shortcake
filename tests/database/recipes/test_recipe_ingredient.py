from shortcake.database.models.ingredients import Ingredient
from shortcake.database.models.recipes import Recipe, RecipeIngredient

from tests.utils import fake_db
from tests.utils.helpers import verify_composite_primary_key


class TestRecipeIngredientModel:
    def test_table_exists(self, postgres_test_db):
        """Entry test to make sure the Recipe table exists"""
        assert postgres_test_db.table_exists("recipe_ingredient")

    def test_fields(self):
        recipe = fake_db.Recipe()
        ingredient = fake_db.Ingredient()

        ingredient_quantity = 4
        ingredient_unit = "cup"

        RecipeIngredient.create(
            recipe=recipe,
            ingredient=ingredient,
            quantity=ingredient_quantity,
            unit=ingredient_unit,
        )

        [recipe_ingredient] = RecipeIngredient.select()

        assert isinstance(recipe_ingredient.recipe, Recipe)
        assert isinstance(recipe_ingredient.ingredient, Ingredient)
        assert isinstance(recipe_ingredient.quantity, float)
        assert isinstance(recipe_ingredient.unit, str)

        assert recipe_ingredient.recipe == recipe
        assert recipe_ingredient.ingredient == ingredient
        assert recipe_ingredient.quantity == ingredient_quantity
        assert recipe_ingredient.unit == ingredient_unit

    def test_primary_key(self):
        verify_composite_primary_key(
            Model=RecipeIngredient,
            primary_keys=[RecipeIngredient.recipe, RecipeIngredient.ingredient],
        )
