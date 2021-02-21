from typing import TYPE_CHECKING, List, Optional, Type

import peewee

from . import fake_db

if TYPE_CHECKING:
    from pql.models import BaseModel


def verify_model_association(
    *,
    Parent: Type["BaseModel"],
    Child: Type["BaseModel"],
    parent_field: str,
    backref: str
):
    """Make sure child.backref properly links parent and child.

    Both Parent and Child _must_ have identically named classes in fake_db

    :param Parent: Parent model
    :param Child: Child model
    :param parent_field: name of field on Child that points to Parent
    :param backref: name of backref from Parent to Child
    """

    parent_name = Parent.__name__
    child_name = Child.__name__

    FakeParent = getattr(fake_db, parent_name)
    FakeChild = getattr(fake_db, child_name)

    parent0 = FakeParent()
    parent1 = FakeParent()
    assert len(Parent.select()) == 2

    child0 = FakeChild(**{parent_field: parent0})
    child1 = FakeChild(**{parent_field: parent0})
    child2 = FakeChild(**{parent_field: parent1})
    child3 = FakeChild(**{parent_field: parent1})
    assert len(Child.select()) == 4

    parent0_children = getattr(parent0, backref)
    parent1_children = getattr(parent1, backref)

    # Make sure de-duplication doesn't mask problems
    assert len(parent0_children) == 2
    assert len(parent1_children) == 2

    assert set(parent0_children) == {child0, child1}
    assert set(parent1_children) == {child2, child3}


def verify_deletion_cascade(
    *,
    Parent: Type["BaseModel"],
    Child: Type["BaseModel"],
    parent_field: str,
    backref: Optional[str]
):
    """Make sure child objects are deleted when their parents are (i.e.
    cascading deletion)

    Both Parent and Child _must_ have identically named classes in fake_db

    :param Parent: Parent model
    :param Child: Child model
    :param parent_field: name of field on Child that points to Parent
    :param backref: name of backref from Parent to Child. If None, the backref
                    is not tested
    """

    parent_name = Parent.__name__
    child_name = Child.__name__

    FakeParent = getattr(fake_db, parent_name)
    FakeChild = getattr(fake_db, child_name)

    # If there is a self-reference in the model, we need to augment the number
    # of expected objects
    num_parents = 2 if Parent is Child else 0
    assert len(Child.select()) == 0
    assert len(Parent.select()) == 0

    parent0 = FakeParent()
    parent1 = FakeParent()
    assert len(Parent.select()) == 2

    FakeChild(**{parent_field: parent0})
    FakeChild(**{parent_field: parent0})
    child2 = FakeChild(**{parent_field: parent1})
    child3 = FakeChild(**{parent_field: parent1})
    assert len(Child.select()) == 4 + num_parents

    parent0.delete_instance()
    num_parents = 1 if Parent is Child else 0
    assert len(Child.select()) == 2 + num_parents

    if backref is not None:
        parent1_children = getattr(parent1, backref)
        assert set(parent1_children) == {child2, child3}

    parent1.delete_instance()
    assert len(Child.select()) == 0


def verify_deletion_set_null(
    *,
    Parent: Type["BaseModel"],
    Child: Type["BaseModel"],
    parent_field: str,
    backref: Optional[str]
):
    """Make sure child objects' foreign keys are set null when the parent rows
    they reference are deleted

    Both Parent and Child _must_ have identically named classes in fake_db

    :param Parent: Parent model
    :param Child: Child model
    :param parent_field: name of field on Child that points to Parent
    :param backref: name of backref from Parent to Child. If None, the backref
                    is not tested
    """

    parent_name = Parent.__name__
    child_name = Child.__name__

    FakeParent = getattr(fake_db, parent_name)
    FakeChild = getattr(fake_db, child_name)

    # If there is a self-reference in the model, we need to augment the number
    # of expected objects
    num_parents = 2 if Parent is Child else 0
    assert len(Child.select()) == 0
    assert len(Parent.select()) == 0

    parent0 = FakeParent()
    parent1 = FakeParent()
    assert len(Parent.select()) == 2

    child0 = FakeChild(**{parent_field: parent0})
    child1 = FakeChild(**{parent_field: parent0})
    child2 = FakeChild(**{parent_field: parent1})
    child3 = FakeChild(**{parent_field: parent1})
    assert len(Child.select()) == 4 + num_parents

    assert child0.parent == child1.parent == parent0
    assert child2.parent == child3.parent == parent1

    parent0.delete_instance()
    num_parents = 1 if Parent is Child else 0
    assert len(Child.select()) == 4 + num_parents

    child0 = refresh_record(child0)
    child1 = refresh_record(child1)
    child2 = refresh_record(child2)
    child3 = refresh_record(child3)
    assert child0.parent is child1.parent is None
    assert child2.parent == child3.parent == parent1

    if backref is not None:
        parent1_children = getattr(parent1, backref)
        assert set(parent1_children) == {child2, child3}

    parent1.delete_instance()
    assert len(Child.select()) == 4

    child0 = refresh_record(child0)
    child1 = refresh_record(child1)
    child2 = refresh_record(child2)
    child3 = refresh_record(child3)
    assert child0.parent is child1.parent is None
    assert child2.parent is child3.parent is None


def verify_single_primary_key(primary_key: peewee.Field):
    assert primary_key.primary_key is True


def verify_composite_primary_key(
    *, Model: Type["BaseModel"], primary_keys=List[peewee.Field]
):
    # noinspection PyProtectedMember
    composite_key = Model._meta.primary_key
    assert isinstance(composite_key, peewee.CompositeKey)

    primary_key_names = [key.name for key in primary_keys]
    composite_key_fields = list(composite_key.field_names)
    assert primary_key_names == composite_key_fields


def refresh_record(record: "BaseModel"):
    # noinspection PyProtectedMember
    return type(record).get(record._pk_expr())
