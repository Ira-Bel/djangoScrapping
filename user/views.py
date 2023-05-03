from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from .tasks import send_confirmation_email


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_confirmation_email.delay(user.id)

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


def logout_view(request):
    logout(request)
    return redirect('start')
