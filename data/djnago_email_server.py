from django.core.mail import send_mail, EmailMessage
from django.conf import settings


def send(subject, message, html_message, recipients):
    send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients,
        fail_silently=False,
    )


def email(subject, body, to, cc=None, bcc=None, reply_to=None):
    msg = EmailMessage(
        subject=subject,
        to=to,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        cc=cc,
        bcc=bcc,
        reply_to=reply_to,
    )
    msg.send()


def mail(subject, message, to):
    msg = EmailMessage(
        subject=subject,
        to=[to],
        body=message,
        from_email=settings.EMAIL_HOST_USER,
    )
    msg.send()