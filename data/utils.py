import datetime
import random

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone


def generate_otp():
    return random.randrange(111111, 999999, 6)


def time_set():
    timezone.localtime(timezone.now()) + datetime.timedelta(minutes=15)


def send_email(otp, email_id):
    msg = EmailMessage(
        subject='Forget Password',
        to=[email_id],
        body=f"your Code is:{otp} ",
        from_email=settings.EMAIL_HOST_USER, )
    msg.send()


def my_clipboard():
    # try:
    pass
    #     verify_otp = VerifyOtp.objects.get(user=user)
    #     resend = request.POST.get('resend')
    #     print(resend )
    #     if resend:
    #         print('hello')
    #         if expiry > timezone.localtime(timezone.now()):
    #             otp = verify_otp.otp
    #             msg = EmailMessage(
    #                 subject='Forget Password',
    #                 to=[email_id],
    #                 body=f"your Code is:{otp} ",
    #                 from_email=settings.EMAIL_HOST_USER, )
    #             msg.send()
    #         elif expiry < timezone.localtime(timezone.now()):
    #             obj.delete()
    #             otp = generate_otp()
    #             exp = timezone.localtime(timezone.now()) + datetime.timedelta(minutes=15)
    #             obj = VerifyOtp(otp=otp, user=user, exp=exp)
    #             obj.save()
    #             send_forgot_pass_email(otp, email_id)
    #             context['secondOTP'] = "Your OTP has been Sent"
    #
    #         else:
    #             context['greater15'] = "Your Last OTP was Expired, Please Resend OTP"
