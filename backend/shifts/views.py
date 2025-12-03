from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from rest_framework_simplejwt.views import TokenObtainPairView
from .token import CustomTokenObtainPairSerializer  # 👈 yahi se aa raha hai

from .models import Employee, Shift
from .serializers import EmployeeSerializer, ShiftSerializer


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShiftListCreateView(generics.ListCreateAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Shift.objects.all()
        employee_id = self.request.query_params.get('employee')
        date = self.request.query_params.get('date')

        if employee_id:
            qs = qs.filter(employee__id=employee_id)
        if date:
            qs = qs.filter(date=date)

        user = self.request.user
        if not user.is_staff:
            try:
                emp = user.employee_profile
                qs = qs.filter(employee=emp)
            except Employee.DoesNotExist:
                qs = qs.none()
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_staff:
            try:
                emp = user.employee_profile
            except Employee.DoesNotExist:
                raise PermissionDenied("You are not linked to any employee record.")
            if serializer.validated_data['employee'] != emp:
                raise PermissionDenied("You can only create shifts for your own employee record.")
        serializer.save(created_by=user)


class ShiftDeleteView(generics.DestroyAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        user = self.request.user
        if user.is_staff:
            instance.delete()
            return
        if hasattr(instance.employee, 'user') and instance.employee.user == user:
            instance.delete()
            return
        raise PermissionDenied("You do not have permission to delete this shift.")
