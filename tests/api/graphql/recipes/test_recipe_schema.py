from strawberry.type import StrawberryOptional

from shortcake.api.graphql.recipes import Recipe


class TestRecipeSchema:
    def test_nullability(self):
        fields = {field.name: field for field in Recipe._type_definition.fields}

        assert not isinstance(fields["id"].type, StrawberryOptional)
        assert not isinstance(fields["name"].type, StrawberryOptional)
        assert isinstance(fields["description"].type, StrawberryOptional)
        assert not isinstance(fields["ingredients"].type, StrawberryOptional)
        assert not isinstance(fields["steps"].type, StrawberryOptional)
