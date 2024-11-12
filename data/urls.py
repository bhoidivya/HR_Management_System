from django.urls import path
from . import views
from .views import about_us, register

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('data/', views.data_view, name='data'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employee/', views.emp_table, name='emp_table'),
    path('department/', views.dep_table, name='dep_table'),
    path('department/add/', views.add_dep_view, name='add_dep'),
    path('department/<int:id>/edit/', views.edit_dep_view, name='edit_dep'),
    path('department/<int:id>/delete/', views.delete_dep_view, name='delete_dep'),
    path('employee/<int:id>/edit/', views.edit_emp_view, name='edit_emp'),
    path('employee/<int:id>/delete/', views.delete_emp_view, name='delete_emp'),
    path('employee/add/', views.add_emp_view, name='add_emp'),
    path('password/', views.pass_change_view, name='pass_change'),
    path('email/', views.send_mail, name='send_mail'),
    path('email_message/', views.send_EmailMessage, name='email_message'),
    path('forget/', views.forget_password_views, name='forget_page'),
    path('resend_otp/<int:id>/', views.resend_otp_view, name='resend_otp'),
    path('code/<int:id>/', views.code_views, name='code_page'),
    path('pass_reset/', views.pass_reset_view, name='pass_reset'),
    path('code1/<str:first_name>/', views.code1_views, name='code1'),
    path('change/', views.change_view, name='change'),
    path('about_us/', about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    # path('hr/', views.HR, name='hr'),
    path('register/', register, name='register'),
    path('attendance_list/attendance_create/', views.create_attendance, name='attendance-create'),
    path('attendance_list/', views.attendance_list, name='attendance-list'),
    path('leave_request_list/leave_request_create/', views.create_leave_request, name='leave-create'),
    path('leave_request_list/', views.leave_request_list, name='leave_request'),
    path('intern_list/intern/', views.intern, name='intern'),
    path('intern_list/', views.intern_list, name='intern_list'),
    path('blog/', views.blog, name='blog'),
    path('blog_single/', views.blog_single, name='blog_single'),
    path('management/', views.management_view, name='management'),
    
    

]
