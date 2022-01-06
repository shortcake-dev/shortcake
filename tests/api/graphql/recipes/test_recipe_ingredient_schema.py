from strawberry.type import StrawberryOptional

from shortcake.api.graphql.recipes import RecipeIngredient


class TestRecipeIngredientSchema:
    def test_nullability(self):
        fields = {
            field.name: field for field in RecipeIngredient._type_definition.fields
        }

        assert not isinstance(fields["recipe"].type, StrawberryOptional)
        assert not isinstance(fields["ingredient"].type, StrawberryOptional)
        assert not isinstance(fields["measurement"].type, StrawberryOptional)
        assert isinstance(fields["modifier"].type, StrawberryOptional)
