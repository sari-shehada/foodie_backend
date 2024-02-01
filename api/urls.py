from django.urls import include, path
import api.views.user_views as user_views
import api.views.restaurant_views as restaurant_views
import api.views.meal_views as meal_views
import api.views.category_views as category_views

api_urls = [
    path('users/login/', user_views.login),
    path('users/signup/', user_views.createAccount),
    path('users/<int:id>/', user_views.getById),
    path('restaurants/login/', restaurant_views.login),
    path('restaurants/<int:id>/', restaurant_views.getById),
    path('restaurants/', restaurant_views.getDisplayRestaurants),
    path('restaurants/search/', restaurant_views.RestaurantSearch.as_view()),
    path('restaurants/<int:id>/meals/', restaurant_views.getRestaurantMeals),
    path('restaurants/<int:restaurantId>/addMeal/',
         restaurant_views.addMealToRestaurant),
    path('rateMeal/', meal_views.rateMeal),
    path('categories/', category_views.getDisplayCategories),
    path('meals/<int:mealId>/', meal_views.getMealDetails),
    path('meals/<int:mealId>/toggleFavorite/', user_views.toggleFavoriteMeal),
    path('meals/<int:mealId>/addPromotion/', meal_views.addPromotionToMeal),
    path('meals/<int:mealId>/removePromotion/', meal_views.removeMealPromotion),
]
