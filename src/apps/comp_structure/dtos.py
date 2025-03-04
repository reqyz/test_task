from dataclasses import dataclass


@dataclass
class DepartmentDTO:
    id: int
    name: str


@dataclass
class EmployeeDTO:
    id: int
    fio: str
    position: str
    hire_date: str
    salary: float
    department_id: int
