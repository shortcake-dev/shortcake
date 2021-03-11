from uuid import UUID

from shortcake.api.graphql import schema

from tests.utils import fake_db


class TestRecipeResolver:
    def test_fields(self):
        query = """
            query($id: ID!) {
                recipe(id: $id) {
                    id,
                    name,
                    description,
                    ingredients {
                        ingredient {
                            id
                        }
                    }
                }
            }
        """

        db_recipe = fake_db.Recipe()
        db_ingredient = fake_db.Ingredient()
        _db_recipe_ingredient = fake_db.RecipeIngredient(
            recipe=db_recipe, ingredient=db_ingredient
        )

        result = schema.execute_sync(
            query=query, variable_values={"id": str(db_recipe.id)}
        )

        assert not result.errors
        recipe = result.data["recipe"]

        assert UUID(recipe["id"]) == db_recipe.id
        assert recipe["name"] == db_recipe.name
        assert recipe["description"] == db_recipe.description
        assert UUID(recipe["ingredients"][0]["ingredient"]["id"]) == db_ingredient.id


class TestRecipesResolver:
    def test_ids(self):
        query = """
            {
                recipes {
                    id
                }    
            }
        """

        db_recipes = [fake_db.Recipe(), fake_db.Recipe(), fake_db.Recipe()]

        result = schema.execute_sync(query)
        assert not result.errors

        graphql_recipe_ids = [UUID(recipe["id"]) for recipe in result.data["recipes"]]
        db_recipe_ids = [recipe.id for recipe in db_recipes]

        assert graphql_recipe_ids == db_recipe_ids
