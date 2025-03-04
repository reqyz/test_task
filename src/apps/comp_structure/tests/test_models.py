import pytest

from apps.comp_structure.models import Department


@pytest.mark.django_db
def test_create_department():
    root = Department.add_root(name="корень")
    assert root.name == "корень"
    assert root.is_root()


@pytest.mark.django_db
def test_add_child_department():
    root = Department.add_root(name="Root Department")
    child = root.add_child(name="Child Department")
    assert child.name == "Child Department"
    assert child.get_parent() == root


@pytest.mark.django_db
def test_delete_department():
    root = Department.add_root(name="Root Department")
    root.delete()
    assert not Department.objects.filter(name="Root Department").exists()
