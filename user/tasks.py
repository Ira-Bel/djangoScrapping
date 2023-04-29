from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from celery import shared_task


@shared_task
def send_confirmation_email(user_id):
    user = User.objects.get(id=user_id)
    message = render_to_string(
        "registration/email_confirm.html",
        {
            "domain": "127.0.0.1:8000",
            "user": user,
            "uid": user.id,
            "token": default_token_generator.make_token(user)
        }
    )
    send_mail(
        subject="Подтвердите регистрацию",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        message=message
    )
