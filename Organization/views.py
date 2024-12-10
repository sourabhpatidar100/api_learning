from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse
import json
# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from .utils import build_response
from .models import Project, Company, Employee, APIMonitor
from .serializers import ProjectSerializerV1, EmployeeSerializerV1, ProjectUpdateSerializer
from rest_framework import status
from datetime import datetime
# Create your views here.
from datetime import date, timedelta
from django.db.models import Avg, Max, Min
from rest_framework.permissions import IsAuthenticated


class BaseView(GenericAPIView):
    permission_classes = [IsAuthenticated]

class ExampleView(APIView):
    throttle_classes = [UserRateThrottle]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


class EmployeesByExperienceAPI(BaseView):
    

    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    'years_of_experience',  # Name of the parameter
                    openapi.IN_QUERY,  # Location of the parameter (query string)
                    description="Years of experiance .Must be a positive integer.",
                    type=openapi.TYPE_INTEGER,  # Data type
                    required=True,  # Optional parameter
                ),
            ]
        )
    

    def get(self, request,company_code):
        '''
        This is to get Employees which has mensioned yeares of experince
        '''


        # company_code = request.query_params.get('company_code')
        years_of_experience = request.query_params.get('years_of_experience')

        

        try:
            # Validate input
            if not company_code or not years_of_experience:
                return Response(
                    {"error": "Both 'company_code' and 'years_of_experience' are required."},
                    status=status.HTTP_400_BAD_REQUES
                )
            years_of_experience = int(years_of_experience)
        
            if years_of_experience <= 0:
                return build_response(
                message="years_of_experience should be positive integer", 
                data={},
                status=status.H
            )
            # Fetch the company
            company = Company.objects.get(company_code=company_code)

            # Calculate the date for filtering
            experience_cutoff_date = date.today() - timedelta(days=years_of_experience * 365)

            # Filter employees based on experience
            employees = Employee.objects.filter(
                organisation=company,
                doj__lte=experience_cutoff_date
            )

            # Serialize employee data
            serializer = EmployeeSerializerV1(employees, many=True)

            return build_response(message='success',data=serializer.data, status=status.HTTP_200_OK)

        except Company.DoesNotExist:
            return build_response(
                message=f"Company with code {company_code} does not exist.", 
                data={},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return build_response(
                message="years_of_experience' must be a valid integer.", 
                data={},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return build_response(
                message=str(e) ,
                data={},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CompanyDetailsAPI(BaseView):
    serializer_class =EmployeeSerializerV1
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

    def get(self, request, company_code):
        try:
            # Fetch the company by company_code
            company = Company.objects.get(company_code=company_code)

            # Fetch associated employees and projects
            employees = Employee.objects.filter(organisation=company)
            projects = Project.objects.filter(organisation=company)

            # Serialize data
            employee_data = EmployeeSerializerV1(employees, many=True).data 
            project_data = ProjectSerializerV1(projects, many=True).data

            # Prepare response
            response = {
                "company_name": company.company_name,
                "company_code": company.company_code,
                "number_of_employees": company.number_of_employees,
                "projects": project_data,
                "employees": employee_data,
            }
            return build_response(message="Success", status=status.HTTP_200_OK, data=response)

        except Company.DoesNotExist:
            return Response(
                {"error": f"Company with code {company_code} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
class AddEmployeeAPI(BaseView):
    serializer_class = EmployeeSerializerV1
    """
    API to add an employee to a company using company_code or company_name.
    """
    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    'company_code',  # Name of the parameter
                    openapi.IN_QUERY,  # Location of the parameter (query string)
                    description="Must be valid code",
                    type=openapi.TYPE_INTEGER,  # Data type
                    required=True,  # Optional parameter
                ),
            ]
        )
    def post(self, request):
        with transaction.atomic():
        # Extract company code from request data
            company_code = request.query_params.get('company_code')
            if not company_code:
                return Response({"error": "Company code is required."}, status=400)
            
            # Check if the company exists
            try:
                company = Company.objects.get(company_code=company_code)
            except Company.DoesNotExist:
                return Response({"error": "Company with the provided code does not exist."}, status=404)
            
            project_code =request.data['project'] 
            try:
                project = Project.objects.get(project_code=project_code)
            except project.DoesNotExist:
                return Response({"error": "project_code with the provided code does not exist."}, status=404)
            
            # Exclude company_code from employee data and associate the company
            employee_data = request.data.copy()
            employee_data.pop("company_code", None)  # Remove company_code from the input
            employee_data["organisation"] = company.id  # Add the organisation field
            employee_data["project_code"] = project.project_code  # Add the organisation field

            
            # Serialize the employee data
            serializer = EmployeeSerializerV1(data=employee_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
    



    
class UpdateEmployeeProjectAPI(BaseView):
    serializer_class = ProjectUpdateSerializer
    def put(self, request):
        # Extract inputs from the request data
        employee_code = request.data.get("employee_code")
        project_code = request.data.get("project_code")

        


        # Validate that both inputs are provided
        if not employee_code or not project_code:
            return Response(
                {"error": "Both employee_id and project_code are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch the employee
        try:
            employee = Employee.objects.get(employee_code=employee_code)
        except Employee.DoesNotExist:
            return Response(
                {"error": f"Employee with ID {employee_code} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        # Check if the employee is already assigned to a project
        if employee.project_code is not None:
            return Response(
                {"error": "Employee is already assigned to a project. Update denied."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Fetch the project using the project_code
        try:
            project = Project.objects.get(project_code=project_code)
        except Project.DoesNotExist:
            return Response(
                {"error": f"Project with code {project_code} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        if project.organisation != employee.organisation:
            return Response(
                {"error": "Bhai kya kar raha he employee kisi aur company me he aur project dusri comapny ka he"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update the employee's project field
        employee.project_code = project
        employee.save()

        # Serialize the updated employee object
        serializer = EmployeeSerializerV1(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
from django.db import transaction

class AverageSalaryAPIView(BaseView):
    serializer_class =EmployeeSerializerV1

    @transaction.atomic
    def get(self, request, company_codes):

        # Check if the company exists
        try:
            company = Company.objects.get(company_code=company_codes)
        except Company.DoesNotExist:
            return Response(
                {"error": f"Company with code {company_codes} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        today =datetime.today()
        APIMonitor.objects.create(api_name="AverageSalaryAPIView", employee="Deepak",hit_time=today )
        # Calculate average salary for employees in the company
        avg_salary = Employee.objects.filter(organisation=company).aggregate(Avg('salary'))['salary__avg']
        max_salary = Employee.objects.filter(organisation=company).aggregate(Max('salary'))['salary__max']
        min_salary = Employee.objects.filter(organisation=company).aggregate(Min('salary'))['salary__min']


        
        if avg_salary is None:
            return Response(
                {"message": f"No employees found for company with code {company_codes}."},
                status=status.HTTP_200_OK,
            )
        
        # Return the average salary
        return Response(
            {
                "company_code": company_codes,
                "company_name": company.company_name,
                "average_salary": round(avg_salary, 2),
                "max_salary": round(max_salary, 2),
                "min_salary": round(min_salary, 2),



            },
            status=status.HTTP_200_OK,
        )

    # def get(self, request, company_codes):
    #     # Split the comma-separated company codes
    #     company_code_list = [int(code.strip()) for code in company_codes.split(",") if code.strip().isdigit()]
        
    #     if not company_code_list:
    #         return Response(
    #             {"error": "Invalid or empty company codes provided."},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
        
    #     # Fetch companies based on the provided codes
    #     companies = Company.objects.filter(company_code__in=company_code_list)
    #     if not companies.exists():
    #         return Response(
    #             {"error": "No companies found for the provided codes."},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
        
    #     # Initialize response data
    #     response_data = []
    #     for company in companies:
    #         avg_salary = Employee.objects.filter(organisation=company).aggregate(Avg('salary'))['salary__avg']
    #         response_data.append({
    #             "company_code": company.company_code,
    #             "company_name": company.company_name,
    #             "average_salary": round(avg_salary, 2) if avg_salary is not None else None,
    #         })

    #     return Response(response_data, status=status.HTTP_200_OK)

        

    # def post(self, request, company_code):
    #     # Extract company code, name, and employee data from request
    #     # company_code = request.data.get('company_code')
    #     employee_data = request.data.get('employee_data')

    #     if not employee_data:
    #         return Response(
    #             {"error": "Employee data is required."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     try:
    #         # Fetch the company using company_code or company_name
    #         if company_code:
    #             company = Company.objects.get(company_code=company_code)
    #         else:
    #             return Response(
    #                 {"error": "Either 'company_code' or 'company_name' is required."},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )

    #         # Add organisation reference to employee data
    #         employee_data['organisation'] = company.id

    #         # Serialize and save the employee data
    #         serializer = EmplyoeeSerializerV1(data=employee_data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     except Company.DoesNotExist:
    #         return Response(
    #             {"error": "Company not found."},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
        




