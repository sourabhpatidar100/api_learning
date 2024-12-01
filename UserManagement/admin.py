from django.contrib import admin

# Register your models here.
from .models import Project, Company, Employee


admin.site.register(Project)
admin.site.register(Company)
admin.site.register(Employee)
