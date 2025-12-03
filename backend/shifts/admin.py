from django.contrib import admin
from .models import Employee, Shift
# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'employee_code', 'department', 'user')
  search_fields = ('name', 'employee_code')

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
  list_display = ('id', 'employee', 'date', 'start_time', 'end_time', 'created_by', 'created_at')
  list_filter = ('date', 'employee__department')
  search_fields = ('employee__name', 'employee__employee_code')