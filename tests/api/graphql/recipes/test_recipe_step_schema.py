from strawberry.type import StrawberryOptional

from shortcake.api.graphql.recipes import RecipeStep


class TestRecipeStepSchema:
    def test_nullability(self):
        fields = {field.name: field for field in RecipeStep._type_definition.fields}

        assert not isinstance(fields["recipe"].type, StrawberryOptional)
        assert not isinstance(fields["step_index"].type, StrawberryOptional)
        assert not isinstance(fields["text"].type, StrawberryOptional)
