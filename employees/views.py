from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Employee, WorkShift
from .serializers import EmployeeSerializer, WorkShiftSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404

class CreateEmployeeView(APIView):
    @swagger_auto_schema(
        request_body=EmployeeSerializer,
        responses={
            201: openapi.Response("Employee created successfully", EmployeeSerializer),
            400: "Validation Error"
        }
    )
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Employee created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EmployeeListView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    # Cho phép filter và search
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'department': ['exact'],          # lọc theo phòng ban
        'start_date': ['gte', 'lte'],     # lọc ngày bắt đầu sau/trước
        'position': ['exact'],            # lọc theo vị trí
    }
    ordering_fields = ['start_date', 'name']  # cho phép sort
    ordering = ['start_date']  # mặc định sort theo ngày bắt đầu

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('department', openapi.IN_QUERY, description="Lọc theo phòng ban", type=openapi.TYPE_STRING),
            openapi.Parameter('start_date__gte', openapi.IN_QUERY, description="Ngày bắt đầu >= ...", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('start_date__lte', openapi.IN_QUERY, description="Ngày bắt đầu <= ...", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('position', openapi.IN_QUERY, description="Lọc theo vị trí", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Sort theo field (vd: start_date, -start_date, name, -name)", type=openapi.TYPE_STRING),
        ]
    )

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UpdateWorkShiftView(APIView):
    serializer_class = WorkShiftSerializer
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['employee_id', 'work_day', 'shift'],
            properties={
                'employee_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID nhân viên'),
                'work_day': openapi.Schema(type=openapi.TYPE_STRING, format="date", description='Ngày làm việc YYYY-MM-DD'),
                'shift': openapi.Schema(type=openapi.TYPE_STRING, description='Ca làm việc (morning, afternoon, full_day)'),
            },
        ),
        responses={200: WorkShiftSerializer()}
    )
    def post(self, request):
        employee_id = request.data.get("employee_id")
        work_day = request.data.get("work_day")
        shift = request.data.get("shift")

        if not employee_id or not work_day or not shift:
            return Response({"error": "employee_id, work_day, shift là bắt buộc"},
                            status=status.HTTP_400_BAD_REQUEST)

        # kiểm tra nhân viên tồn tại
        employee = get_object_or_404(Employee, id=employee_id)

        obj, created = WorkShift.objects.update_or_create(
            employee=employee,
            work_day=work_day,
            defaults={"shift": shift}
        )

        serializer = WorkShiftSerializer(obj)
        message = "created" if created else "updated"
        return Response(
            {"message": f"Lịch làm việc đã {message}", "data": serializer.data},
            status=status.HTTP_200_OK
        )