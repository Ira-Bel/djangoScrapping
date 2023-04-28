from django.contrib.auth.tokens import default_token_generator
from django.core import serializers
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserRegistrationSerializer, MessageSerializer, \
    GoodsShowSerializer, GoodsPriceSerializer
from ..models import Goods
from django.contrib.auth.models import User
from rest_framework import generics, status
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class ShowUsersAPIViews(APIView):

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            serializer_message = MessageSerializer(data={
                "message": render_to_string(
                    "registration/email_confirm.html",
                    {
                        "domain": "127.0.0.1:8000",
                        "user": user,
                        "uid": user.id,
                        "token": default_token_generator.make_token(user)
                    }
                )
            })
            if serializer_message.is_valid():
                serializer_message.save()
                send_mail(
                    subject="Подтвердите регистрацию",
                    from_email="NewUserIra@yandex.ru",
                    recipient_list=[user.email],
                    message=serializer_message.validated_data['message']
                )

                return Response({"detail": "Регистрация прошла успешно. Проверьте свою электронную почту, чтобы подтвердить свою учетную запись."}, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                return Response(serializer_message.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAPIView(generics.GenericAPIView):
    serializer_class = serializers.Serializer

    def get(self, request, uid: str, token: str):
        user = get_object_or_404(User, id=int(uid))

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save(update_fields=["is_active"])
            return HttpResponse("<h1>Вы можете войти<h1>")

        return HttpResponse("<h1>Неверный токен!!!<h1>")


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Неверные учетные данные."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = serializers.Serializer

    def get(self, request):
        logout(request)
        return redirect('start')


class ShowAllGoodsAPIView(APIView):

    def get(self, request):
        items = Goods.objects.all().values("name", "description", "image_link").distinct()
        print(items)
        serializer = GoodsShowSerializer(items, many=True)
        return Response(serializer.data)


class GoodsPriceAPIView(APIView):
    def get(self, request, name):
        goods = Goods.objects.filter(name=name).order_by('date')

        dates = [good.date for good in goods]
        prices = [good.price for good in goods]
        min_price = min(prices)
        current_price = prices[-1]

        # Convert dates to numerical format
        dates_num = mdates.date2num(dates)

        # Plot graph
        fig, ax = plt.subplots()
        ax.plot_date(dates_num, prices, fmt='-', xdate=True)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
        ax.yaxis.set_major_locator(plt.MultipleLocator(1))
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.set_title('Price vs Date')

        # Return the plot as a PNG image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        serializer = GoodsPriceSerializer({
            'image': f'data:image/png;base64,{image}',
            'current_price': current_price,
            'min_price': min_price
        })
        return Response(serializer.data)
