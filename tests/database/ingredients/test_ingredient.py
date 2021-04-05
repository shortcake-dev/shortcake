from uuid import UUID

from shortcake.database.models.recipes import Ingredient

from tests.utils.helpers import verify_single_primary_key


class TestIngredientModel:
    def test_table_exists(self, postgres_test_db):
        """Entry test to make sure the Recipe table exists"""
        assert postgres_test_db.table_exists("ingredient")

    def test_fields(self):
        ingredient_name = "Potato"

        Ingredient.create(name=ingredient_name)

        [ingredient] = Ingredient.select()

        assert isinstance(ingredient.id, UUID)
        assert isinstance(ingredient.name, str)

        assert ingredient.name == ingredient_name

    def test_primary_key(self):
        verify_single_primary_key(Ingredient.id)

    def test_nullability(self):
        assert not Ingredient.id.null
        assert not Ingredient.name.null
