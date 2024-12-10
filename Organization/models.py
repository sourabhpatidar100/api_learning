from django.db import models

# Create your models here.


class Company(models.Model):
    company_code = models.IntegerField()  # Removed max_length
    company_name = models.CharField(max_length=100)
    number_of_employees = models.IntegerField(null=True, blank=True)
    is_exits = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.company_name}"


class Project(models.Model):
    project_code = models.IntegerField(primary_key=True,unique=True)  # Fixed invalid field
    project_name = models.CharField(max_length=100)  # Added max_length
    organisation = models.ForeignKey(Company, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.project_name}"


class Employee(models.Model):
    employee_code = models.IntegerField()  # Removed max_length
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    doj = models.DateField()
    dol = models.DateField(null=True, blank=True)  # Allowed null and blank for current employees
    organisation = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    project_code = models.ForeignKey('Project',to_field='project_code', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class APIMonitor(models.Model):
    api_name = models.CharField(max_length=1000)
    employee = models.CharField(max_length=100)
    hit_time = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.api_name} was hit by -{self.employee}- on -{self.hit_time}"
