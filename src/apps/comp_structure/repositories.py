from django.db.models import QuerySet

from apps.comp_structure.dtos import DepartmentDTO
from apps.comp_structure.factories import DepartmentFactory
from apps.comp_structure.models import Department, Employee


class DepartmentRepository:

    @staticmethod
    def get_root_departments() -> list[DepartmentDTO]:
        departments = Department.get_root_nodes().values('id', 'name')
        return [DepartmentFactory.dict_to_dto(dept) for dept in departments]

    @staticmethod
    def get_children(department_id: int) -> list[DepartmentDTO]:
        department = Department.objects.get(id=department_id)
        children = department.get_children().values('id', 'name')
        return [DepartmentFactory.dict_to_dto(child) for child in children]


class EmployeeRepository:
    # Тут, конечно, смешиваем контексты джанги и репозиториев, это не очень хорошо,
    # но изобретать велосипед вместо Page через лимиты и офсеты не хотелось, поэтому такой компромисс
    @staticmethod
    def get_employees_by_department_query(department_id: int) -> QuerySet:
        employees = Employee.objects.filter(department_id=department_id).order_by('id').values('id', 'fio', 'position',
                                                                                               'hire_date',
                                                                                               'salary',
                                                                                               'department_id')
        return employees
