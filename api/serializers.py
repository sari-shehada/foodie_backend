from rest_framework import serializers
from api.models import FoodieUser, Meal, MealCategory, MealRating, Restaurant


class FoodieUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodieUser
        fields = "__all__"


class FoodieUserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodieUser
        exclude = ['password']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        # fields = "__all__"
        exclude = ['password']


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = "__all__"


class MealCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealCategory
        fields = "__all__"


class RestaurantCategoryMealsSerializer(serializers.ModelSerializer):
    meals = serializers.SerializerMethodField(read_only=True)

    def get_meals(self, category):
        restaurantId = self.context.get('restaurantId')
        meals = Meal.objects.filter(
            category=category.pk, restaurant=restaurantId)
        # TODO: Keep an eye
        return MealSerializer(meals, many=True, context={'request': self.context.get('request')}).data

    class Meta:
        model = MealCategory
        fields = "__all__"


class MealRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealRating
        fields = "__all__"
