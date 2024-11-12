from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Department(models.Model):
    dep_name = models.CharField(max_length=25, verbose_name="Department Name")

    def __str__(self):
        return str(self.dep_name)


GENDER_CHOICES = (
    ("0", "Male"),
    ("1", "Female"),
)


class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, default=None, null=True)
    dep = models.ForeignKey('Department', null=True,blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=None, null=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default=None, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.age}'

    class Meta:
        ordering = ['id']


class VerifyOtp(models.Model):
    otp = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    emp = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True)
    exp = models.DateTimeField()


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField(null=True, blank=True)

    # def __str__(self):
    #     return f"Attendance of {self.employee.first_name} on {self.date}"
    def __str__(self):
        if self.employee:  # Check if employee is not None
            return f"Attendance of {self.employee.first_name} on {self.date}"
        else:
            return f"Attendance on {self.date} (No Employee)"


class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    # def __str__(self):
    #     return f"Leave Request for {self.employee.first_name}"
    def __str__(self):
        if self.employee:  # Check if employee is not None
            return f"Leave Request for {self.employee.first_name}"
        else:
            return f"Leave Request (No Employee)"


class Intern(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    skills = models.TextField()
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.name

