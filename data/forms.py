from django import forms
from data.models import Department, Employee, Attendance, LeaveRequest, Intern


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"
        
class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = "__all__"

class InternForm(forms.ModelForm):
    class Meta:
        model = Intern
        fields = "__all__"