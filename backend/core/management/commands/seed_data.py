from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from shifts.models import Employee

User = get_user_model()

class Command(BaseCommand):
    help = "Seed admin, normal user and reviewer + employee records"

    def handle(self, *args, **options):
        # Admin
        admin_email = "sakshigharat701@gmail.com"
        admin_password = "password"  # you can change this if you want
        admin_qs = User.objects.filter(username=admin_email)
        if not admin_qs.exists():
            admin = User.objects.create_user(
                username=admin_email,
                email=admin_email,
                password=admin_password,
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS(f"Admin user created: {admin_email}"))
        else:
            self.stdout.write(self.style.WARNING(f"Admin user already exists: {admin_email}"))

        # Normal user + linked Employee
        user_email = "user@example.com"
        user_password = "User@123"
        user_qs = User.objects.filter(username=user_email)
        if not user_qs.exists():
            user = User.objects.create_user(
                username=user_email,
                email=user_email,
                password=user_password,
                is_staff=False,
                is_superuser=False,
            )
            emp, created = Employee.objects.get_or_create(
                user=user,
                defaults={
                    "name": "Normal User",
                    "employee_code": "EMP001",
                    "department": "IT",
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created normal user + employee: {user_email} / {user_password} (employee {emp.employee_code})"
                )
            )
        else:
            user = user_qs.first()
            emp_qs = Employee.objects.filter(user=user)
            if not emp_qs.exists():
                emp = Employee.objects.create(
                    user=user,
                    name="Normal User",
                    employee_code="EMP001",
                    department="IT",
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Linked existing user to employee: {user_email} -> {emp.employee_code}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING("Normal user already exists and linked to employee.")
                )
    
        reviewer_email = "hire-me@anshumat.org"
        reviewer_password = "HireMe@2025!"
        reviewer_qs = User.objects.filter(username=reviewer_email)
        if not reviewer_qs.exists():
            reviewer = User.objects.create_user(
                username=reviewer_email,
                email=reviewer_email,
                password=reviewer_password,
                is_staff=True,        # reviewer behaves like admin/staff
                is_superuser=False,
            )
            reviewer_emp, _ = Employee.objects.get_or_create(
                user=reviewer,
                defaults={
                    "name": "Reviewer",
                    "employee_code": "EMP999",
                    "department": "HR",
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Reviewer user created: {reviewer_email} / {reviewer_password} (employee {reviewer_emp.employee_code})"
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Reviewer user already exists: {reviewer_email}")
            )
