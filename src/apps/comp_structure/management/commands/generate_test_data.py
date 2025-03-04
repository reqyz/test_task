import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker

from apps.comp_structure.models import Department, Employee


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--departments', type=int, default=25)
        parser.add_argument('--employees', type=int, default=100000)
        parser.add_argument('--max-depth', type=int, default=5)

    def handle(self, *args, **options):
        fake = Faker()
        num_departments = options['departments']
        num_employees = options['employees']
        max_depth = options['max_depth']

        self.stdout.write(
            self.style.SUCCESS(f'Добавляю {num_departments} департаментов с глубиной дерева {max_depth}...'))
        departments = self._generate_departments(num_departments, max_depth, fake)

        self.stdout.write(self.style.SUCCESS(f'Добавляю {num_employees} сотрудников...'))
        self._generate_employees(num_employees, departments, fake)

        self.stdout.write(self.style.SUCCESS('База заполнена!'))

    @staticmethod
    def get_dispersion(num_departments):
        def _fib():
            a, b = 1, 2
            while True:
                yield a
                a, b = b, a + b

        rv = []
        for f in _fib():
            if (sum(rv) + f) >= num_departments:
                s = num_departments - sum(rv)
                rv.append(s)
                break
            rv.append(f)
        return rv

    def _generate_departments(self, num_departments, max_depth, fake):
        check_dep = Department.objects.first()
        if check_dep:
            return
        departments = []
        current_depth = 1
        deps = []
        for lvl_deps_num in self.get_dispersion(num_departments):
            if not deps:
                deps = [Department.add_root(name=fake.unique.company())]
            new_deps = []
            for dep_num in range(lvl_deps_num):
                parent = random.choice(deps)
                while True:
                    try:
                        child = parent.add_child(name=fake.unique.company())
                        new_deps.append(child)
                        departments.append(child)
                        break
                    except IntegrityError:
                        # https://github.com/django-treebeard/django-treebeard/issues/53
                        # Тут баг django-treebeard, даже транзакцией не фиксится
                        continue
            if current_depth < max_depth:
                deps = new_deps
                current_depth += 1
        return departments

    def _generate_employees(self, num_employees, departments, fake):
        check_emp = Employee.objects.first()
        if check_emp:
            return

        employees = []
        batch_size = 5000
        rest = num_employees

        for i in range(num_employees):
            department = random.choice(departments)

            employee = Employee(
                fio=fake.name(),
                position=fake.job(),
                hire_date=fake.date_between(start_date='-10y', end_date='today'),
                salary=random.randint(30000, 200000),
                department=department,
            )
            employees.append(employee)

            if len(employees) >= batch_size:
                Employee.objects.bulk_create(employees)
                rest -= batch_size
                self.stdout.write(self.style.SUCCESS(f'Добавил {num_employees} сотрудников, осталось {rest}'))
                employees = []

        if employees:
            Employee.objects.bulk_create(employees)
