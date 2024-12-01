from django.urls import path
from django.contrib import admin

from .views import ProjectAPI, ProjectAPIUpdate, CompanyAPI, CompanyWithCount, EmployeeAPI, EmloyeeAge

urlpatterns = [
path('project/crud/', ProjectAPI.as_view(),name="project-get-api"),
path('project/update/<int:id>/', ProjectAPIUpdate.as_view(),name="project-put-api"),
path('company/crud/<int:id>/', CompanyAPI.as_view(),name="company-get-api"),
path('company/crudV2/<int:number_of_objects>/', CompanyWithCount.as_view(),name="company-get2-api"),
]

urlpatterns += [
    path('Emplyoee/', EmployeeAPI.as_view(), name='projectEmployee-query-count'),
    path('EmplyoeeAge/', EmloyeeAge.as_view(), name='EmployeeAge-query-count'),
]