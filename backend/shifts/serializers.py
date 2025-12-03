from rest_framework import serializers
from .models import Employee, Shift
from datetime import datetime, timedelta

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'employee_code', 'department']


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ['id', 'employee', 'date', 'start_time', 'end_time', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def validate(self, data):
        """
        TODO: implement validation steps below - return data if valid,
              raise serializers.ValidationError(...) if not.
        Steps:
        1) Ensure date, start_time, end_time, employee exist (if missing, let field-level validation handle it)
        2) Combine date + times into start_dt and end_dt
        3) Check end_dt > start_dt (else error "End time must be after start time.")
        4) Check duration >= 4 hours (else error "Shift must be at least 4 hours long.")
        5) Query existing shifts for same employee and same date.
           - If self.instance exists, exclude it.
           - For each existing shift, compute existing_start/existing_end and check overlap:
             if start_dt < existing_end and end_dt > existing_start -> raise error "Shift overlaps..."
        6) If all good, return data
        """
        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        employee = data.get('employee')
        if not (date and start_time and end_time and employee):
            return data  
        start_dt = datetime.combine(date, start_time)
        end_dt = datetime.combine(date, end_time)
        if end_dt <= start_dt:
            raise serializers.ValidationError("End time must be after start time.")
        if (end_dt - start_dt) < timedelta(hours=4):
            raise serializers.ValidationError("Shift must be at least 4 hours long.")
        qs = Shift.objects.filter(employee=employee, date=date)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        for s in qs:
            existing_start = datetime.combine(s.date, s.start_time)
            existing_end = datetime.combine(s.date, s.end_time)
            if start_dt < existing_end and end_dt > existing_start:
                raise serializers.ValidationError("Shift overlaps with an existing shift for this employee on the same date.")
        return data

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)
