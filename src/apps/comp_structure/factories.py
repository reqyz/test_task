from apps.comp_structure.dtos import DepartmentDTO, EmployeeDTO


class DepartmentFactory:

    @classmethod
    def dict_to_dto(cls, department_dict: dict) -> DepartmentDTO:
        return DepartmentDTO(id=department_dict['id'], name=department_dict['name'])

    @classmethod
    def dto_to_dict(cls, department: DepartmentDTO) -> dict:
        return {"id": department.id, "name": department.name}

    @classmethod
    def dtos_to_dicts(cls, departments: list[DepartmentDTO]) -> list[dict]:
        return [cls.dto_to_dict(dept) for dept in departments]


class EmployeeFactory:
    @classmethod
    def dict_to_dto(cls, employee_dict: dict) -> EmployeeDTO:
        return EmployeeDTO(
            id=employee_dict['id'],
            fio=employee_dict['fio'],
            position=employee_dict['position'],
            hire_date=employee_dict['hire_date'].isoformat(),
            salary=float(employee_dict['salary']),
            department_id=employee_dict['department_id'],
        )

    @classmethod
    def dicts_to_dtos(cls, employee_dict: list[dict]) -> list[EmployeeDTO]:
        return [cls.dict_to_dto(emp) for emp in employee_dict]

    @classmethod
    def query_to_dict(cls):
        ...

    @classmethod
    def dto_to_dict(cls, employee: EmployeeDTO) -> dict:
        return {
            "id": employee.id,
            "fio": employee.fio,
            "position": employee.position,
            "hire_date": employee.hire_date,
            "salary": employee.salary,
            "department_id": employee.department_id,
        }

    @classmethod
    def dtos_to_dicts(cls, employees: list[EmployeeDTO]) -> list[dict]:
        return [cls.dto_to_dict(emp) for emp in employees]
