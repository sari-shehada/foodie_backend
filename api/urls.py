from django.urls import include, path
from api import views

api_urls = [
    path('', views.sayHello),
]
