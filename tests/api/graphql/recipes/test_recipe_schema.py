from shortcake.api.graphql.recipes import Recipe


class TestRecipeSchema:
    def test_nullability(self):
        fields = {field.name: field for field in Recipe._type_definition.fields}

        assert not fields["id"].is_optional
        assert not fields["name"].is_optional
        assert fields["description"].is_optional
        assert not fields["ingredients"].is_optional
        assert not fields["steps"].is_optional
