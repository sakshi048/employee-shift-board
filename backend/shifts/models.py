from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Employee(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, related_name = 'employee_profile')
    name = models.CharField(max_length = 150)
    employee_code = models.CharField(max_length = 50, unique=True)
    department = models.CharField(max_length = 100, blank=True)
    def __str__(self):        
        return f"{self.name} ({self.employee_code})"
    
class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='shifts') 
    date = models.DateField()  
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add= True)
    
    class Meta:
      ordering = ['date', 'start_time']
      indexes = [
          models.Index(fields = ['employee', 'date'])
      ]

    def __str__(self):
      
      return f"{self.employee} - {self.date} {self.start_time}-{self.end_time}"
