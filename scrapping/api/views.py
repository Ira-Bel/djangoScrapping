from django.contrib.auth.tokens import default_token_generator
from django.core import serializers
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserRegistrationSerializer, \
    GoodsShowSerializer, GoodsPriceSerializer
from ..models import Goods
from django.contrib.auth.models import User
from rest_framework import generics, status
from user.tasks import send_confirmation_email
from django.shortcuts import get_object_or_404


class ShowUsersAPIViews(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = True
        user.save()
        send_confirmation_email.delay(user.id)
        return Response(
            {
                "detail": "Регистрация прошла успешно."
                          "Проверьте свою электронную почту, чтобы подтвердить свою учетную запись."
            },
            status=status.HTTP_201_CREATED
        )


class ActivateAPIView(generics.GenericAPIView):

    def get(self, request, uid: str, token: str):
        user = get_object_or_404(User, id=int(uid))

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save(update_fields=["is_active"])
            return HttpResponse("<h1>Вы можете войти<h1>")

        return HttpResponse("<h1>Неверный токен!!!<h1>")


class ShowAllGoodsAPIView(APIView):

    def get(self, request):
        items = Goods.objects.all().values("name", "description", "image_link").distinct()
        serializer = GoodsShowSerializer(items, many=True)
        return Response(serializer.data)


class GoodsPriceAPIView(APIView):
    def get(self, request, name):
        goods = Goods.objects.filter(name=name).order_by("date")

        dates = [good.date for good in goods]
        prices = [good.price for good in goods]
        min_price = min(prices)
        current_price = prices[-1]

        serializer = GoodsPriceSerializer(
            {
                "data": {
                    "dates": dates,
                    "prices": prices,
                },
                "min_price": min_price,
                "current_price": current_price,
            }
        )
        return Response(serializer.data)
