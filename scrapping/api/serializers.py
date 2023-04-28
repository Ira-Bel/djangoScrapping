from rest_framework import serializers
from ..models import Goods
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    message = serializers.CharField()

    class Meta:
        model = User
        fields = ['message']


class GoodsShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ["name", "description", "image_link"]


class GoodsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    date = serializers.DateField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class GoodsPriceSerializer(serializers.Serializer):
    image = serializers.CharField()
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2)
