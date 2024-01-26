from rest_framework import serializers
from api.models import FoodieUser


class FoodieUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodieUser
        fields = "__all__"


class FoodieUserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodieUser
        fields = ['username', 'firstName', 'lastName', 'phoneNumber']
