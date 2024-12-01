from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100, null=True , blank=True)
    project_id = models.IntegerField(unique=True, null=True , blank=True)
    project_dis = models.TextField(null=True , blank=True)


class Company(models.Model):
    name = models.CharField(max_length=100, null=True , blank=True)
    category =models.CharField(max_length=100, null=True, blank=True)
    number_of_employees = models.IntegerField(null=True, blank=True)
    is_exits = models.BooleanField(default=True)


class Employee(models.Model):
    first_name = models.CharField(max_length =100, null =True, blank =True)
    last_name = models.CharField(max_length =100, null =True, blank =True)
    dob = models.DateField(null=True, blank=True) 
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return f"{str(self.first_name)} - {str(self.last_name)}"


