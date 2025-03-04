from django.core.validators import MinValueValidator
from django.db import models
from treebeard.mp_tree import MP_Node


class Department(MP_Node):
    name = models.CharField(max_length=100)

    node_order_by = ['name']

    def __str__(self):
        return self.name


class Employee(models.Model):
    fio = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return self.fio
