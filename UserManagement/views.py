from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
import json
# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import GenericAPIView

from .utils import build_response
from .models import Project, Company, Employee
from .serializers import ProjectSerializer, CompanySerializer, EmplyoeeSerializer
from rest_framework import status
from datetime import datetime


class ProjectAPI(GenericAPIView):
    serializer_class = ProjectSerializer
    def get(self, request):
        projects = Project.objects.all()
        length =projects.count()
        serializer = ProjectSerializer(projects, many=True)
        response = {
            "count":length,
            "result" : serializer.data
        }
        return JsonResponse(response)


    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProjectAPIUpdate(GenericAPIView):
    serializer_class = ProjectSerializer

    def put(self, request, id):
        """
        Handle full updates to a project instance identified by its primary key.
        """
        # Fetch the project instance
        project = Project.objects.get(id=id)
        serializer = ProjectSerializer(project, data=request.data)  # Full update

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id, *args, **kwargs):
        project = Project.objects.get(id=id) # Retrieves the object using the primary key
        project.delete()  # Deletes the object
        return Response(
            {"detail": "Project deleted successfully."}, 
            status=status.HTTP_204_NO_CONTENT
        )

class CompanyAPI(GenericAPIView):
    serializer_class =CompanySerializer
    def get(self, request ,id):
        company = Company.objects.get(id=id)
        serializer =CompanySerializer(company)
        return Response(serializer.data)
    
class CompanyWithCount(GenericAPIView):
    def get(self, request ,number_of_objects):
        company = Company.objects.all()[:number_of_objects]
        serializer = CompanySerializer(company, many = True)
        return Response(serializer.data)

class EmployeeAPI(GenericAPIView):
    serializer_class =EmplyoeeSerializer
    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    'count',  # Name of the parameter
                    openapi.IN_QUERY,  # Location of the parameter (query string)
                    description="Number of employees to retrieve. Must be a positive integer.",
                    type=openapi.TYPE_INTEGER,  # Data type
                    required=False,  # Optional parameter
                ),
            ]
        )

    def get(self, request, *args, **kwargs):
        
        count = request.query_params.get('count')
        employees = Employee.objects.all()
        try:
            if count:
                count = int(count)
                if count < 1:
                    return Response(
                        {"error": "'count' must be a positive integer."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                employees = Employee.objects.all()[:count]

            # Serialize the data
            serializer = EmplyoeeSerializer(employees, many=True)
            
            return build_response(status=status.HTTP_200_OK, message="Success",data=serializer.data,len=count)

        except ValueError:
            return Response(
                {"error": "'count' must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

class EmloyeeAge(GenericAPIView):
    def get(self, request,*args, **kwargs):
        today = datetime.today().date()

        # Get all employees
        employees = Employee.objects.filter(is_active=True).order_by("-id")

        # Filter employees who are younger than 25 years
        filtered_employees = [
            employee for employee in employees
            if (today - employee.dob).days // 365 < 25
        ]
        serializer = EmplyoeeSerializer(filtered_employees, many=True)

        # Prepare the custom response data
        response_data = {
            "count": len(filtered_employees),
            "data": serializer.data
        }
        return Response(response_data)
