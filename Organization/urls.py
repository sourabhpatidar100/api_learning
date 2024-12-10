from django.contrib import admin
from django.urls import path, include


from .views import CompanyDetailsAPI, EmployeesByExperienceAPI, AddEmployeeAPI, UpdateEmployeeProjectAPI, AverageSalaryAPIView

urlpatterns = [
    path('company/<int:company_code>/', CompanyDetailsAPI.as_view(), name='company-details'),
    path('api/employees-by-experience/<int:company_code>/', EmployeesByExperienceAPI.as_view(), name ='employee-details'),
    path('api/employeesAdd/', AddEmployeeAPI.as_view(), name ='employee-add'),
    path('api/employeesProjectAdd/', UpdateEmployeeProjectAPI.as_view(), name ='employee-project-add'),
    # path('api/company/emplyoeeAvgSalary/<int:company_code>', AverageSalaryAPIView.as_view(), name ='Avg-Salary'),
    path('api/average-salaries/<str:company_codes>/', AverageSalaryAPIView.as_view(), name='average-salaries'),
]

