from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from apps.comp_structure.factories import DepartmentFactory
from apps.comp_structure.repositories import DepartmentRepository, EmployeeRepository


def department_tree(request):
    root_departments = DepartmentRepository.get_root_departments()
    return render(request, 'department_tree.html', {'root_departments': root_departments})


def get_children(request):
    department_id = request.GET.get('department_id')
    page = request.GET.get('page', 1)
    per_page = 20

    children = DepartmentRepository.get_children(department_id)
    children_data = DepartmentFactory.dtos_to_dicts(children)

    employees = EmployeeRepository.get_employees_by_department_query(department_id)
    paginator = Paginator(employees, per_page)
    employees_page = paginator.page(page)

    return JsonResponse({
        'children': children_data,
        'employees': list(employees_page.object_list),
        'has_next': employees_page.has_next(),
        'has_previous': employees_page.has_previous(),
        'current_page': employees_page.number,
        'total_pages': paginator.num_pages,
    })
