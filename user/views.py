from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse

from .forms import UserRegistrationForm
from django.contrib.auth.models import User


def create_message(user) -> str:
    message = render_to_string(
        "registration/email_confirm.html",
        {
            "domain": "127.0.0.1:8000",
            "user": user,
            "uid": user.id,
            "token": default_token_generator.make_token(user)
        }
    )

    return message


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_mail(
                subject="Подтвердите регистрацию",
                from_email="NewUserIra@yandex.ru",
                recipient_list=[user.email],
                message=create_message(user)
            )

            return redirect("main")
    else:
        form = UserRegistrationForm()
    return render(request, "registration/sign-up.html", {"form": form})


def activate(request, uid: str, token: str):

    user = get_object_or_404(User, id=int(uid))

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=["is_active"])
        return HttpResponse("<h1>Вы можете войти<h1>")

    return HttpResponse("<h1>Неверный токен!!!<h1>")
