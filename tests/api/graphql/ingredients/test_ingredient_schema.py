from strawberry.type import StrawberryOptional

from shortcake.api.graphql.ingredients import Ingredient


class TestIngredientSchema:
    def test_nullability(self):
        fields = {field.name: field for field in Ingredient._type_definition.fields}

        assert not isinstance(fields["id"].type, StrawberryOptional)
        assert not isinstance(fields["name"].type, StrawberryOptional)
