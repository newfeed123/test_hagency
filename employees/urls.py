from django.urls import path
from .views import CreateEmployeeView, EmployeeListView, UpdateWorkShiftView

urlpatterns = [
    path('create/', CreateEmployeeView.as_view(), name='create_employee'),
    path('', EmployeeListView.as_view(), name='list_employee'),
    path('work-shift/', UpdateWorkShiftView.as_view(), name='update_work_shift'),
]
