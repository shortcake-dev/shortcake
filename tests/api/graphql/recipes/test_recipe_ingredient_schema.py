import pytest

from shortcake.api.graphql.recipes import RecipeIngredient


class TestRecipeIngredientSchema:
    @pytest.mark.xfail(reason="shortcake-dev/shortcake#54")
    def test_nullability(self):
        fields = {
            field.name: field for field in RecipeIngredient._type_definition.fields
        }

        assert not fields["recipe"].is_optional
        assert not fields["ingredient"].is_optional
        assert not fields["measurement"].is_optional
        assert fields["modifier"].is_optional
