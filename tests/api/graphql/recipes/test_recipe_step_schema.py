from shortcake.api.graphql.recipes import RecipeStep


class TestRecipeStepSchema:
    def test_nullability(self):
        fields = {field.name: field for field in RecipeStep._type_definition.fields}

        assert not fields["recipe"].is_optional
        assert not fields["stepIndex"].is_optional
        assert not fields["text"].is_optional
