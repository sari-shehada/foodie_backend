from django.contrib import admin
from api.models import FoodieUser, Meal, MealCategory, MealRating, Restaurant, UserFavoriteMeal

admin.site.register(Restaurant)
admin.site.register(MealCategory)
admin.site.register(Meal)
admin.site.register(FoodieUser)
admin.site.register(MealRating)
admin.site.register(UserFavoriteMeal)
