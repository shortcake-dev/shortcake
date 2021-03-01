from uuid import UUID

from shortcake.api.graphql import schema

from tests.utils import fake_db


class TestIngredientResolver:
    def test_fields(self):
        query = """
            query($id: ID!) {
                ingredient(id: $id) {
                    id,
                    name
                }
            }
        """

        db_ingredient = fake_db.Ingredient()

        result = schema.execute_sync(
            query=query, variable_values={"id": str(db_ingredient.id)}
        )

        assert not result.errors
        ingredient = result.data["ingredient"]

        assert UUID(ingredient["id"]) == db_ingredient.id
        assert ingredient["name"] == db_ingredient.name


class TestIngredientsResolver:
    def test_ids(self):
        query = """
            {
                ingredients {
                    id
                }    
            }
        """

        db_ingredients = [
            fake_db.Ingredient(),
            fake_db.Ingredient(),
            fake_db.Ingredient(),
        ]

        result = schema.execute_sync(query)
        assert not result.errors

        graphql_ingredient_ids = [
            UUID(ingredient["id"]) for ingredient in result.data["ingredients"]
        ]
        db_ingredient_ids = [ingredient.id for ingredient in db_ingredients]

        assert graphql_ingredient_ids == db_ingredient_ids
