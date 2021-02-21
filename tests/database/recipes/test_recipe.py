from uuid import UUID

from shortcake.database.models.recipes import Recipe

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

    def test_primary_key(self):
        verify_single_primary_key(Recipe.id)
