from uuid import UUID

from shortcake.database.models.recipes import Recipe

from tests.utils import fake_db
from tests.utils.helpers import verify_single_primary_key


class TestRecipeModel:
    def test_table_exists(self, postgres_test_db):
        """Entry test to make sure the Recipe table exists"""
        assert postgres_test_db.table_exists("recipe")

    def test_fields(self):
        recipe_name = "Strawberry Shortcake"
        recipe_description = "A delicious cake"

        Recipe.create(name=recipe_name, description=recipe_description)

        [recipe] = Recipe.select()

        assert isinstance(recipe.id, UUID)
        assert isinstance(recipe.name, str)
        assert isinstance(recipe.description, str)

        assert recipe.name == recipe_name
        assert recipe.description == recipe_description

    def test_ingredients_property(self):
        ingredient_1 = fake_db.Ingredient()
        _ingredient_2 = fake_db.Ingredient()
        ingredient_3 = fake_db.Ingredient()

        recipe = fake_db.Recipe()

        _recipe_ingredient_1 = fake_db.RecipeIngredient(
            recipe=recipe, ingredient=ingredient_1
        )
        _recipe_ingredient_2 = fake_db.RecipeIngredient(
            recipe=recipe, ingredient=ingredient_3
        )

        assert len(recipe.ingredients) == 2
        assert recipe.ingredients == ingredient_1, ingredient_3

    def test_steps_property(self):
        recipe = fake_db.Recipe()

        num_steps = 3
        steps = [fake_db.RecipeStep(recipe=recipe) for _ in range(num_steps)]

        assert len(recipe.steps) == num_steps
        assert list(recipe.steps) == steps

    def test_primary_key(self):
        verify_single_primary_key(Recipe.id)

    def test_nullability(self):
        assert not Recipe.id.null
        assert not Recipe.name.null
        assert Recipe.description.null
