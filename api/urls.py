from django.urls import include, path
import api.views.user_views as user_views
import api.views.restaurant_views as restaurant_views

api_urls = [
    path('users/login/', user_views.login),
    path('users/signup/', user_views.createAccount),
    path('users/<int:id>/', user_views.getById),
    path('restaurants/login/', restaurant_views.login),
    path('restaurants/<int:id>/', restaurant_views.getById),
    path('restaurants/', restaurant_views.getDisplayRestaurants),
]
