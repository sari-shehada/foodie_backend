from rest_framework import serializers
from api.models import FoodieUser, Meal, MealCategory, MealRating, Restaurant, UserFavoriteMeal


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


class MealWithUserSerializer(serializers.ModelSerializer):
    isInFavorites = serializers.SerializerMethodField(read_only=True)
    myRating = serializers.SerializerMethodField(read_only=True)

    def get_isInFavorites(self, meal):
        userId = self.context.get('userId')
        favorites = UserFavoriteMeal.objects.filter(meal=meal.pk, user=userId)
        return len(favorites) > 0

    def get_myRating(self, meal):
        userId = self.context.get('userId')
        ratingObject = MealRating.objects.filter(
            meal=meal.pk, user=userId).first()
        return ratingObject.rating if ratingObject != None else None

    class Meta:
        model = Meal
        fields = "__all__"


class MealCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MealCategory
        fields = "__all__"


class UserFavoriteMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteMeal
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
