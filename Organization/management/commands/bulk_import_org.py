from django.core.management.base import BaseCommand
from Organization.models import Company, Project, Employee
from datetime import date
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Creates sample data for Company, Project, and Employee models"

    def handle(self, *args, **kwargs):
        # Create 10 companies
        companies = []
        for i in range(10):
            company = Company.objects.create(
                company_code=i + 100,
                company_name=fake.company(),
                is_exits=True
            )
            companies.append(company)
        self.stdout.write("10 companies created successfully.")

        # Create 10 projects for each company
        projects = []
        for company in companies:
            for j in range(10):
                while True:  # Loop until a unique project_code is found
                    project_code = random.randint(3000, 9999)
                    if not Project.objects.filter(project_code=project_code).exists():
                        break  # Exit the loop when a unique project_code is found
                
                # Create the project with the unique project_code
                project = Project.objects.create(
                    project_code=project_code,
                    project_name=fake.bs().title(),
                    organisation=company
                )
                projects.append(project)
        self.stdout.write(f"{len(projects)} projects created successfully (10 per company).")

        # Create 100 employees
        for i in range(100):
            company = random.choice(companies)
            project = random.choice([p for p in projects if p.organisation == company])

            # Generate random data
            dob = fake.date_of_birth(minimum_age=18, maximum_age=60)
            doj = fake.date_between(start_date=dob.replace(year=dob.year + 18), end_date="today")
            dol = None if random.choice([True, False]) else fake.date_between(start_date=doj, end_date="today")

            Employee.objects.create(
                employee_code=1000 + i + 1,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                dob=dob,
                email=fake.unique.email(),
                salary=random.randint(30000, 120000),
                is_active=dol is None,
                doj=doj,
                dol=dol,
                organisation=company,
                project_code=project
            )

        # Update number_of_employees for each company
        for company in companies:
            company.number_of_employees = Employee.objects.filter(organisation=company).count()
            company.save()

        self.stdout.write("100 employees created successfully and assigned to companies and projects.")
