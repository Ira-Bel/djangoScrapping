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


class GoodsShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = ["name", "description", "image_link"]


class GraphSerializer(serializers.Serializer):
    dates = serializers.ListSerializer(required=True, child=serializers.DateTimeField())
    prices = serializers.ListSerializer(required=True, child=serializers.DecimalField(max_digits=10, decimal_places=2))


class GoodsPriceSerializer(serializers.Serializer):
    data = GraphSerializer()
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2)
