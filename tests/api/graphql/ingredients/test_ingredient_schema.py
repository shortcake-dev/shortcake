from shortcake.api.graphql.ingredients import Ingredient


class TestIngredientSchema:
    def test_nullability(self):
        fields = {field.name: field for field in Ingredient._type_definition.fields}

        assert not fields["id"].is_optional
        assert not fields["name"].is_optional
