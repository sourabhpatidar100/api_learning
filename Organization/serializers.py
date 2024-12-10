from rest_framework import serializers

from .models import Project, Company, Employee



class ProjectSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class CompanySerializerV1(serializers.ModelSerializer):
    class Meta:
        model =Company
        fields = '__all__'   

class EmployeeSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields ='__all__'

class ProjectUpdateSerializer(serializers.ModelSerializer):
    project_code = serializers.IntegerField()


    class Meta:
        model = Employee
        fields = ['employee_code', 'project_code']
