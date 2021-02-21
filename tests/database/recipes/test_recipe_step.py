from shortcake.database.models.recipes import Recipe, RecipeStep

from tests.utils import fake_db
from tests.utils.helpers import verify_composite_primary_key


class TestRecipeStepModel:
    def test_table_exists(self, postgres_test_db):
        """Entry test to make sure the Recipe table exists"""
        assert postgres_test_db.table_exists("recipe_step")

    def test_fields(self):
        recipe = fake_db.Recipe()
        step_index = 12

        text = "Beat the eggs into the batter"

        RecipeStep.create(
            recipe=recipe,
            step_index=step_index,
            text=text,
        )

        [recipe_step] = RecipeStep.select()

        assert isinstance(recipe_step.recipe, Recipe)
        assert isinstance(recipe_step.step_index, int)
        assert isinstance(recipe_step.text, str)

        assert recipe_step.recipe == recipe
        assert recipe_step.step_index == step_index
        assert recipe_step.text == text

    def test_primary_key(self):
        verify_composite_primary_key(
            Model=RecipeStep, primary_keys=[RecipeStep.recipe, RecipeStep.step_index]
        )
