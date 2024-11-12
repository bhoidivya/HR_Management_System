from typing import Set
from urllib import request
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from data.models import Employee, Department, VerifyOtp, Attendance, LeaveRequest, Intern


class AgeFilter(SimpleListFilter):
    title = 'Age'
    parameter_name = 'Age_filter'

    def lookups(self, request, model_admin):
        my_list = [
            # (None,"All"),
            ('minor', "Minor"),
            ('young', 'Young'),
            ('senior', 'Senior')
        ]
        return my_list

    def queryset(self, request, queryset):
        if self.value() == 'minor':
            return queryset.filter(age__lt=18)
        elif self.value() == 'young':
            return queryset.filter(age__gt=18, age__lt=50)
        elif self.value() == 'senior':
            return queryset.filter(age__gt=50)


class SalaryFilter(SimpleListFilter):
    title = 'Salary'
    parameter_name = 'sl_filter'

    def lookups(self,request, model_admin):
        my_list = [
            ('lt25', '<25000'),
            ('lt50', '<50000'),
            ('gt50', '>50000')
        ]
        return my_list

    def queryset(self, request, queryset):
        if self.value() == 'lt25':
            return queryset.filter(salary__lt=25000)
        elif self.value() == 'lt50':
            return queryset.filter(salary__lt=50000)
        elif self.value() == 'gt50':
            return queryset.filter(salary__gt=50000)



@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id','fname', 'age', 'dep_name', 'f_salary', 'fage', 'is_active')
    list_filter = (AgeFilter, SalaryFilter )



    def fname(self, employee_obj):
        return f'{employee_obj.first_name} {employee_obj.last_name} {employee_obj.age}'

    fname.short_description = 'Full Name'

    def fage(self, employee_obj):
        # print(employee_obj.age)
        # emp : Employee.objects.all().values()
        # print(emp)

        # return format_html(f'<span style="color:red;">{employee_obj.age}</span>')
        if employee_obj.age:
            if employee_obj.age < 18:
                result = "Minor"
            elif 18 < employee_obj.age < 50:
                result = "Young"
            else:
                result = "Senior"
            return format_html(
                f'<b>{employee_obj.age}</b>, <a href="/admin/table_data/employee/?Age_filter={result.lower()}">{result}</a>')
        return employee_obj.age
    fage.short_description = 'Employee age '

    def dep_name(self, obj):
        if obj.dep:
            return format_html(f'<span style="color:red;">{obj.dep.dep_name}</span>')
        return None

    def f_salary(self, emp_obj):
        if emp_obj.salary:
            if emp_obj.salary < 15000:
                return format_html(f'<span style="color:red;">{emp_obj.salary}</span>')
            elif 15000 < emp_obj.salary < 40000:
                return format_html(f'<span style="color:yellow;">{emp_obj.salary} </span>')
            else:
                return format_html(f'<span style="color:green;">{emp_obj.salary}</span>')
        return emp_obj.salary
    f_salary.short_description = 'Employee salary '


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(VerifyOtp)
class VerifyOtpAdmin(admin.ModelAdmin):
    list_display = ['otp', 'user','id']

    def __str__(self):
        return f'{self.otp} {self.user}'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'time_in', 'time_out')
    search_fields = ('employee__name', 'date')
    
    
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'reason')
    search_fields = ('employee__name', 'start_date', 'end_date')
    
@admin.register(Intern)    
class InternAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'skills']
    search_fields = ['name', 'email', 'skills']
    readonly_fields = ['resume']
    