from rest_framework import serializers

from .models import Project, Company, Employee

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model =Company
        fields = '__all__'   

class EmplyoeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields ='__all__'