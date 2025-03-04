from django import forms
from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Department, Employee

# В этом порядке из-за особенностей treebeard и добавления условий сохранения для глубины < 5
DepartmentMoveNodeForm = movenodeform_factory(Department)


class CustomDepartmentMoveNodeForm(DepartmentMoveNodeForm):
    def clean(self):
        cleaned_data = super().clean()

        ref_node_id = cleaned_data.get('_ref_node_id')
        position = cleaned_data.get('_position')

        if ref_node_id and position:
            ref_node = Department.objects.get(id=ref_node_id)
            if position == 'sorted-child':
                depth = ref_node.get_depth() + 1
                if depth > 5:
                    raise forms.ValidationError("Глубина иерархии не может превышать 5 уровней.")

        return cleaned_data


@admin.register(Department)
class DepartmentAdmin(TreeAdmin):
    form = CustomDepartmentMoveNodeForm
    list_display = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('fio', 'position', 'hire_date', 'salary', 'department')
