from cgitb import reset
import datetime
# from multiprocessing import context
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.utils import timezone

from data.forms import DepartmentForm, EmployeeForm, AttendanceForm, LeaveRequestForm, InternForm
from data.models import Employee, Department, VerifyOtp, Attendance, LeaveRequest, Intern
from .djnago_email_server import mail, send, email
from .utils import send_email, generate_otp

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import HttpResponse
from django.contrib import messages

LOGIN_URL = "/login/"


def send_mail(request):
    context = {}
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        html_content = request.POST.get('html')
        try:
            recipient = request.POST.get('recipient').split(',')
            print(recipient)
            send(subject=subject, message=message, html_message=html_content, recipients=recipient)
            context['sended'] = "Mail Sended Successfully."
        except Exception as ex:
            print(ex)
            context['error'] = "please enter valid email"
        # return redirect('/home/')
    template = loader.get_template('email_page.html')
    return HttpResponse(template.render(context, request))


def send_EmailMessage(request):
    context = {}
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        reply_to = request.POST.get('reply_to')
        try:
            cc = request.POST.get('cc').split(',')
            to = request.POST.get('to').split(',')
            bcc = request.POST.get('bcc').split(',')
            email(subject=subject, body=body, to=to, cc=cc, bcc=bcc, reply_to=reply_to)
            context['sended'] = "Email Sended Successfully."
            # return redirect('/home/')
        except Exception as ex:
            print(ex)
            context['error'] = "please enter valid email"
    template = loader.get_template('email_message.html')
    return HttpResponse(template.render(context, request))

  
def forget_password_views(request):
    context = {}
    if request.method == 'POST':
        email_id = request.POST.get('email')
        try:
            user = User.objects.get(email=email_id)
            print(user)
        except Exception as e:
            print(e)
            context['error'] = "Please enter valid email id"
        else:
            if user is not None:
                try:
                    verify_otp = VerifyOtp.objects.get(user=user)
                    if verify_otp.exp > timezone.localtime(timezone.now()):
                        otp = verify_otp.otp
                    else:
                        verify_otp.delete()
                        otp = None
                except:
                    otp = None

                if otp is None:
                    otp = generate_otp()
                    exp = timezone.localtime(timezone.now()) + datetime.timedelta(minutes=15)
                    obj = VerifyOtp(otp=otp, user=user, exp=exp)
                    obj.save()

                send_email(otp, email_id)
                return redirect(f'/code/{user.id}')
    template = loader.get_template('forget_page.html')
    return HttpResponse(template.render(context, request))


def resend_otp_view(id):
    user = User.objects.get(id=id)
    obj = VerifyOtp.objects.get(user=user)
    exp = obj.exp
    otp = obj.otp
    email_id = user.email
    if exp > timezone.localtime(timezone.now()):
        send_email(otp, email_id)
    elif exp < timezone.localtime(timezone.now()):
        obj.delete()
        otp = generate_otp()
        exp = timezone.localtime(timezone.now()) + datetime.timedelta(minutes=15)
        obj = VerifyOtp(otp=otp, user=user, exp=exp)
        obj.save()
        send_email(otp, email_id)
    return redirect(f'/code/{id}')


def code_views(request, id):
    context = {
        'id': id,
    }
    user = User.objects.get(id=id)
    if request.method == 'POST':
        msg = request.POST.get('code')
        try:
            user = User.objects.get(id=id)
        except Exception as e:
            print(e)

        obj = VerifyOtp.objects.get(user=user)
        expiry = obj.exp
        code = str(obj.otp)
        if msg == code:
            if expiry < timezone.localtime(timezone.now()):
                context['greater15'] = "Your Last OTP was Expired, Please Resend OTP"
            else:
                login(request, user)
                obj.delete()
                return redirect('/password/')
        else:
            context['error'] = " Please Enter Valid OTP"

    template = loader.get_template('code_page.html')
    return HttpResponse(template.render(context, request))


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/employee/')
    context = {}
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('/hr/')
        else:
            context['error_msg'] = 'Invalid Login'

    template = loader.get_template('login_page.html')
    return HttpResponse(template.render(context, request))


def logout_view(request):
    logout(request)

    return redirect('/login/')


def home_view(request):
    return render(request, 'home.html')


@login_required(login_url=LOGIN_URL)
def emp_table(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    template = loader.get_template('employee_table.html')
    emp_list = Employee.objects.all()
    dep_list = Department.objects.all()
    age_filter = request.GET.get('Age_filter')
    if age_filter == "young":
        emp_list = emp_list.filter(age__gt=18, age__lte=50)
    elif age_filter == 'minor':
        emp_list = emp_list.filter(age__lte=18)
    elif age_filter == 'senior':
        emp_list = emp_list.filter(age__gt=50)

    salary_filter = request.GET.get('sl_filter')
    if salary_filter == 'lt20':
        emp_list = emp_list.filter(salary__lt=20000)
    elif salary_filter == 'lt50':
        emp_list = emp_list.filter(salary__lte=50000, salary__gt=20000)
    elif salary_filter == 'gt50':
        emp_list = emp_list.filter(salary__gt=50000)
    
    gender_filter = request.GET.get('gender_filter')
    if gender_filter == "Male":
        emp_list = emp_list.filter(gender="Male")
    elif gender_filter == "Female":
        emp_list = emp_list.filter(gender="Female")
        
    
    dep_filter = request.GET.get('dep_filter')
    if dep_filter !=None:
        try:
            print("YEVSS")
            dep_fil = Department.objects.filter(dep_name=dep_filter).first()
            emp_list = emp_list.filter(dep=dep_fil)
        except:
            print("SDFGHJK")
            pass
    context = {
        "Employee_list": emp_list,
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url="/home/")
def add_emp_view(request):
    dep_list = Department.objects.all()
    context = {
        "Department_list": dep_list
    }
    if request.method == 'POST':
        print("#$$$$$$$$$$$$$", request.POST.get("emp_id"))
        # emp_id = request.POST.get("emp_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        salary = request.POST.get("salary")
        email = request.POST.get("email")
        dep_id = request.POST.get("dep_id")
        print("#########",dep_id)
        is_active = request.POST.get("is_active")
        gender = request.POST.get("gender")
        exist_e = Employee.objects.filter(first_name=first_name,last_name=last_name,email=email).first()
        print(exist_e,"~~~~~~~~~~~~~~~~~~~~~~~",first_name,last_name,age,salary,email,dep_id,is_active,gender)
        if exist_e:
            # exist_e = Employee.objects.filter(id=emp_id).first()
            dep_name = Department.objects.filter(id=dep_id).first()
            print("~~~~~~~~~~~5~~~~~~~~~",exist_e,is_active)
            context = {
                "emp" : exist_e,
            }
            print("@@",context,dep_name.id)
            exist_e.first_name= first_name
            exist_e.last_name = last_name
            exist_e.age = age
            exist_e.salary = salary
            exist_e.email = email
            exist_e.dep = dep_name
            exist_e.is_active = is_active
            exist_e.gender = gender
            exist_e.save()
            print("****",exist_e.gender)
        else:
            new_e = Employee(first_name=first_name,last_name=last_name,age=age,salary=salary,email=email,dep_id=dep_id,is_active=is_active,gender=gender)
            
            new_e.save()
            
        
        # form = EmployeeForm(request.POST)
        # if form.is_valid():
        #     form.save()
        return redirect('/employee/')
    # form = EmployeeForm()
    # context['form'] = form
    
    template = loader.get_template('add_employee.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url="/home/")
def edit_emp_view(request, id):
    dep_list = Department.objects.all()
    # emp_list = Employee.objects.all()
    emp = Employee.objects.get(id=id)
    context = {
        'emp': emp,
        "Department_list": dep_list,
        # "Employee_list" : emp_list
    }

    if request.method == 'POST':
        emp_id = request.POST.get("emp_id")
        print("#$$$$$$$$$$$$$", emp_id)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")
        salary = request.POST.get("salary")
        email = request.POST.get("email")
        dep_id = request.POST.get("dep_id")
        is_active = request.POST.get("is_active")
        gender = request.POST.get("gender")
        exist_e = Employee.objects.filter(id=emp_id).first()
        print(exist_e,"~~~~~~~~~~~~~~~~~~~~~~~",first_name,last_name,age,salary,email,dep_id,is_active,gender)
        if exist_e:
            exist_e = Employee.objects.filter(id=emp_id).first()
            dep_name = Department.objects.filter(id=dep_id).first()
            context = {
                "emp" : exist_e,
            }
            
            print("BEFORE",exist_e)
            print("@@",context,dep_name.id)
            exist_e.first_name= first_name
            exist_e.last_name = last_name
            exist_e.age = age
            exist_e.salary = salary
            exist_e.email = email
            exist_e.dep = dep_name
            exist_e.is_active = is_active
            exist_e.gender = gender
            exist_e.save()
            print("****after",exist_e)
        else:
            new_e = Employee(first_name=first_name,last_name=last_name,age=age,salary=salary,email=email,dep_id=dep_id,is_active=is_active,gender=gender)
            
            new_e.save()
        return redirect('/employee/')
    template = loader.get_template('add_employee.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url="/home/")
def dep_table(request):
    template = loader.get_template('department.html')
    dep_list = Department.objects.all().values()
    context = {
        "Department_list": dep_list
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/login/")
def add_dep_view(request):
    context = {}
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/department/')
    form = DepartmentForm()
    context['form'] = form
    template = loader.get_template('add_department.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url="/home/")
def edit_dep_view(request, id):
    dep = Department.objects.get(id=id)
    context = {
        'dep': dep
    }
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dep)
        if form.is_valid():

            form.save()
        context['msg'] = "Department updated successfully."
    else:
        form = DepartmentForm(instance=dep)
    context['form'] = form
    template = loader.get_template('add_department.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url="/home/")
def delete_dep_view(request,id):
    try:
        dep = Department.objects.get(id=id)
        dep.delete()
    except:
        pass
    return redirect('/department/')


@login_required(login_url="/home/")
def delete_emp_view(request,id):
    try:
        emp = Employee.objects.get(id=id)
        emp.delete()
    except:
        pass
    return redirect('/employee/')

@login_required(login_url=LOGIN_URL)
def pass_reset_view(request):
    context = {}
    if request.method == 'POST':
        email_id = request.POST.get('email')
        try:
            emp = Employee.objects.get(email=email_id)
            print(emp)
        except Exception as e:
            print(e)
            context['error'] = "Please enter valid email id"
        else:
            if emp is not None:
                try:
                    verify_otp = VerifyOtp.objects.get(emp=emp)
                    if verify_otp.exp > timezone.localtime(timezone.now()):
                        otp = verify_otp.otp
                    else:
                        verify_otp.delete()
                        otp = None
                except:
                    otp = None

                if otp is None:
                    otp = generate_otp()
                    exp = timezone.localtime(timezone.now()) + datetime.timedelta(minutes=15)
                    obj = VerifyOtp(otp=otp, emp=emp, exp=exp)
                    obj.save()

                send_email(otp, email_id)
                return redirect(f'/code1/{emp.first_name}')
    template = loader.get_template('reset_password.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_URL)
def change_view(request):
    user = request.user
    context = {}
    if request.method == 'POST':
        pas = request.POST.get('pas')
        c_pass = request.POST.get('c_pas')
        if pas != c_pass:
            context['error'] = "Please enter Match Password"
        else:
            user.set_password(pas)
            user.save()
            context['changed'] = " Password Reset Successfully"
            return redirect('/login/')
    template = loader.get_template('change.html')
    return HttpResponse(template.render(context, request))


def code1_views(request, first_name):
    context = {
        'first_name': first_name,
    }
    emp = Employee.objects.get(first_name=first_name)
    if request.method == 'POST':
        msg = request.POST.get('code')
        try:
            emp = Employee.objects.get(first_name=first_name)
        except Exception as e:
            print(e)

        obj = VerifyOtp.objects.get(emp=emp)
        expiry = obj.exp
        code = str(obj.otp)
        if msg == code:
            if expiry < timezone.localtime(timezone.now()):
                context['greater15'] = "Your Last OTP was Expired, Please Resend OTP"
            else:
                # reset(request, emp)
                reset()
                obj.delete()
                return redirect('/change/')
        else:
            context['error'] = " Please Enter Valid OTP"
            # return redirect('/change/')
    template = loader.get_template('code.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_URL)
def pass_change_view(request):
    user = request.user
    context = {}
    if request.method == 'POST':
        pas = request.POST.get('pas')
        c_pass = request.POST.get('c_pas')
        if pas != c_pass:
            context['error'] = "Please enter Match Password"
        else:
            user.set_password(pas)
            user.save()
            context['changed'] = " Password Changed Successfully"
            return redirect('/login/')
    template = loader.get_template('change_password.html')
    return HttpResponse(template.render(context, request))

from django.shortcuts import render

def about_us(request):
    return render(request, 'about.html')


def contact_us(request):
    # emp = Employee.objects.get(email=email)
    context = {}
    if request.method == 'POST':
        # first_name = request.POST.get('name')
        # email = request.POST.get('email')
        # message = request.POST.get('message')
        
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        try:
            to = request.POST.get('public_user_email')
            print("@@@@@@@@@@@@@",to)
            mail(subject=subject, message=message, to=to)
            # print(subject,message,to)
            # print(request.POST)

            context['sended'] = "Mail Sended Successfully."
            
        except Exception as ex:
            print(ex)
            context['error'] = "please enter valid email"
    template = loader.get_template('contact.html')
    return HttpResponse(template.render(context, request))


    

@login_required(login_url=LOGIN_URL)
def HR(request):
    return render(request, 'HR.html')




def register(request):
    dep_list = Department.objects.all()
    context = {
               "dep_list" : Department.objects.all()
       }
    if request.method == 'POST':
        # emp_id = request.POST.get("emp_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get('email')
        password = request.POST.get('password')
        salary = request.POST.get("salary")
        dep_id = request.POST.get("dep_id")
        phone = request.POST.get("phone")
        print("#########",dep_id)
        is_active = request.POST.get("is_active")
        exist_e = Employee.objects.filter(first_name=first_name,last_name=last_name,email=email).first()
        if exist_e:
            # exist_e = Employee.objects.filter(id=emp_id).first()
            dep_name = Department.objects.filter(id=dep_id).first()
            context = {
                "emp" : exist_e,
            }
            print("@@",context,dep_name.id)
            exist_e.first_name= first_name
            exist_e.last_name = last_name
            exist_e.email = email
            exist_e.password = password
            exist_e.salary = salary
            exist_e.dep = dep_name
            exist_e.is_active = is_active
            exist_e.phone = phone
            exist_e.save()
            print("****",exist_e.gender)
        else:
            new_e = Employee(first_name=first_name,last_name=last_name,email=email,password=password,salary=salary,dep_id=dep_id,is_active=is_active,phone=phone)
            
            new_e.save()
            
        return redirect('/home/')
    
    template = loader.get_template('register.html')
    return HttpResponse(template.render(context, request))


def create_attendance(request):
    emp_list = Employee.objects.all()
    # attendance_list = Attendance.objects.all()
    context = {
        'Employee_list': emp_list,
        # 'Attendance_list' : attendance_list
    }

    if request.method == 'POST':
        attendance_id = request.POST.get("attendance_id")
        emp_first_name = request.POST.get("emp_first_name")
        print(emp_first_name,"!!!!!!!!!!!!!!!!!!!!!!!")
        date = request.POST.get("date")
        time_in = request.POST.get("time_in")
        time_out = request.POST.get("time_out")
        employee = Employee.objects.filter(first_name=emp_first_name).first()
        # attendance_record = Attendance.objects.filter(employee=emp_first_name, date=date).first()
        print(attendance_id,date,time_in,time_out)
        if employee:
            attendance_record = Attendance.objects.filter(employee=employee,date=date).first()
            if attendance_record:
                attendance_record.time_in = time_in
                attendance_record.time_out = time_out
                attendance_record.save()
            else:
                # employee = Employee.objects.get(id=emp_first_name)
                new_attendance = Attendance(employee=employee,date=date,time_in=time_in,time_out=time_out)
                new_attendance.save()
        else:
            pass
        return redirect('/attendance_list/')
    template = loader.get_template('create_attendance.html')
    return HttpResponse(template.render(context, request))


# def attendance_list(request):
#     attendance_records = Attendance.objects.all()
#     # print(attendance_records)
#     return render(request, 'attendance_list.html', {'attendance_records':attendance_records})
  

def attendance_list(request):
    attendance_records = Attendance.objects.all()
    employees = Employee.objects.all()
    context = {
        'attendance_records': attendance_records,
        'employees': employees,
    }
    return render(request, 'attendance_list.html', context)

    
def create_leave_request(request):
    emp_list = Employee.objects.all()
    context = {
        'Employee_list': emp_list,
    }

    if request.method == 'POST':
        leave_request_id = request.POST.get("leave_request_id")
        # print(leave_request_id,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        emp_first_name = request.POST.get("emp_first_name")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason")
        employee = Employee.objects.filter(first_name=emp_first_name).first()
        print(leave_request_id,start_date,end_date,reason)
        if employee:
            leave_record = LeaveRequest.objects.filter(employee=employee,start_date=start_date).first()
            if leave_record:
                leave_record.end_date = end_date
                leave_record.reason = reason
                leave_record.save()
            else:
                new_leave = LeaveRequest(employee=employee,start_date=start_date,end_date=end_date,reason=reason)
                new_leave.save()
        else:
            pass
        return redirect('/leave_request_list/')
    template = loader.get_template('create_leave_request.html')
    return HttpResponse(template.render(context, request))

# def leave_request_list(request):
#     leave_records = LeaveRequest.objects.all()
#     return render(request, 'leave_request_list.html', {'leave_records':leave_records})

def leave_request_list(request):
    leave_records = LeaveRequest.objects.all()
    employees = Employee.objects.all()
    context = {
        'leave_records': leave_records,
        'employees': employees,
    }
    return render(request, 'leave_request_list.html', context)


@login_required(login_url=LOGIN_URL)
def data_view(request):
    emp = Employee.objects.all().order_by('-id')[:5]
    dep = Department.objects.all().order_by('-id')[:5]
    context = {
        'emp': emp,
        'dep': dep,
    }
    user = request.user
    if user.first_name is not None:
        result = user.first_name
    elif user.last_name is not None:
        result = user.last_name
    else:
        result = user.username
    context['uname'] = result
    template = loader.get_template('data.html')
    return HttpResponse(template.render(context, request))


def intern(request):
    context = {}
    if request.method == 'POST':
        intern_id = request.POST.get("intern_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        skills = request.POST.get("skills")
        resume = request.POST.get("resume")
        intern_record = Intern.objects.filter(name=name).first()
        if intern_record:
            intern_record.email = email
            intern_record.phone = phone
            intern_record.skills = skills
            intern_record.resume = resume
        else:
            new_intern = Intern(name=name,email=email,phone=phone,skills=skills,resume=resume)
            new_intern.save()
            
        return redirect('/intern_list')
    template = loader.get_template('intern.html')
    return HttpResponse(template.render(context,request))
            
def intern_list(request):
    interns = Intern.objects.all()
    return render(request, 'intern_list.html', {'interns': interns})


def blog(request):
    return render(request, 'blog.html')

def blog_single(request):
    return render(request, 'blog-single.html')

def management_view(request):
    return render(request, 'management.html')