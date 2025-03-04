import pytest
from django.urls import reverse

from apps.comp_structure.models import Department, Employee


@pytest.mark.django_db
def test_department_tree_view(client):
    root = Department.add_root(name="Root Department")
    url = reverse('department_tree')
    response = client.get(url)
    assert response.status_code == 200
    assert 'root_departments' in response.context
    assert list(response.context['root_departments']) == [{'id': root.id, 'name': 'Root Department'}]


@pytest.mark.django_db
def test_get_children_view(client):
    root = Department.add_root(name="Root Department")
    child = root.add_child(name="Child Department")
    Employee.objects.create(
        fio="John Doe",
        position="Developer",
        hire_date="2023-01-01",
        salary=50000,
        department=root,
    )
    url = reverse('get_children')
    response = client.get(url, {'department_id': root.id})
    assert response.status_code == 200
    assert response.json() == {
        'children': [{'id': child.id, 'name': 'Child Department'}],
        'employees': [{'fio': 'John Doe', 'position': 'Developer'}],
        'has_next': False,
        'has_previous': False,
        'current_page': 1,
        'total_pages': 1,
    }
