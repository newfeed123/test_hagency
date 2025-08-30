from rest_framework import serializers
from .models import Employee, WorkShift

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class WorkShiftSerializer(serializers.ModelSerializer):
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='employee'  # map vào field employee
    )
    class Meta:
        model = WorkShift
        fields = ['employee_id', 'work_day', 'shift']
