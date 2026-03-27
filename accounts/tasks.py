from celery import shared_task
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email, username):
    subject='Welcome to ArtHub!'
    message=f"Hi {username},\n\nYour registration was successful."
    from_email=settings.DEFAULT_EMAIL
    recipient_list=[user_email]
    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_password_reset_email(
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
):
    form = PasswordResetForm()
    form.send_mail(
        subject_template_name=subject_template_name,
        email_template_name=email_template_name,
        context=context,
        from_email=from_email,
        to_email=to_email,
        html_email_template_name=html_email_template_name,
    )