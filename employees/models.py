from django.db import models

# Create your models here.
from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Email không trùng
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    start_date = models.DateField()

    def __str__(self):
        return self.name
    
class WorkShift(models.Model):
    SHIFT_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('full_day', 'Full Day'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="shifts")
    work_day = models.DateField()
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)

    class Meta:
        unique_together = ('employee', 'work_day')  # mỗi ngày 1 lịch/nhân viên

    def __str__(self):
        return f"{self.employee.name} - {self.work_day} - {self.shift}"
    

