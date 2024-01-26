from rest_framework import serializers
from api.models import FoodieUser, Restaurant


class FoodieUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodieUser
        fields = "__all__"


class FoodieUserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodieUser
        fields = ['username', 'firstName', 'lastName', 'phoneNumber']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        # fields = "__all__"
        exclude = ['password']
