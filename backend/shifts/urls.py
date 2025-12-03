from django.urls import path
from .views import EmployeeListView, ShiftListCreateView, ShiftDeleteView, CustomLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
  path('login/', CustomLoginView.as_view(), name='login'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

  path('employees/', EmployeeListView.as_view(), name='employees'),
  path('shifts/', ShiftListCreateView.as_view(), name='shifts'),
  path('shifts/<int:pk>/', ShiftDeleteView.as_view(), name='shift-delete'),
]
