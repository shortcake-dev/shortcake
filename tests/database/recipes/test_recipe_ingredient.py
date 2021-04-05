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

        measurement = "4 cups"
        modifier = "softened"

        RecipeIngredient.create(
            recipe=recipe,
            ingredient=ingredient,
            measurement=measurement,
            modifier=modifier,
        )

        [recipe_ingredient] = RecipeIngredient.select()

        assert isinstance(recipe_ingredient.recipe, Recipe)
        assert isinstance(recipe_ingredient.ingredient, Ingredient)
        assert isinstance(recipe_ingredient.measurement, str)
        assert isinstance(recipe_ingredient.modifier, str)

        assert recipe_ingredient.recipe == recipe
        assert recipe_ingredient.ingredient == ingredient
        assert recipe_ingredient.measurement == measurement
        assert recipe_ingredient.modifier == modifier

    def test_primary_key(self):
        verify_composite_primary_key(
            Model=RecipeIngredient,
            primary_keys=[RecipeIngredient.recipe, RecipeIngredient.ingredient],
        )

    def test_nullability(self):
        assert not RecipeIngredient.recipe.null
        assert not RecipeIngredient.ingredient.null
        assert not RecipeIngredient.measurement.null
        assert RecipeIngredient.modifier.null
