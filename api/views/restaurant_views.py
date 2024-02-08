from collections import ChainMap
from random import choices
import random
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import Meal, Restaurant
from api.serializers import MealSerializer, RestaurantCategoryMealsSerializer, RestaurantSerializer
from rest_framework import generics
import rest_framework.filters as filters


@api_view(['POST'])
def login(request):
    userName = request.data.get('username')
    password = request.data.get('password')
    try:
        user = Restaurant.objects.get(username=userName)
        if (user.password == password):
            return Response(RestaurantSerializer(user).data)
        else:
            return Response(False)
    except Restaurant.DoesNotExist:
        return Response(False)


@api_view(['GET'])
def getById(request, id):
    try:
        user = Restaurant.objects.get(id=id)
    except Restaurant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(RestaurantSerializer(user, context={'request': request}).data)


@api_view(['GET'])
def getDisplayRestaurants(request):
    ids = Restaurant.objects.values_list('pk', flat=True)
    ids = sorted(ids)
    selectedIds = random.sample(ids, k=5 if len(ids) > 5 else len(ids))
    restaurants = Restaurant.objects.filter(id__in=selectedIds)
    return Response(RestaurantSerializer(restaurants, context={'request': request}, many=True).data)


class RestaurantSearch(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    search_fields = ['name']
    filter_backends = [filters.SearchFilter]


@api_view(['GET'])
def getRestaurantMeals(request, id):
    try:
        restaurant = Restaurant.objects.get(id=id)
        meals = Meal.objects.filter(
            restaurant=restaurant.pk)

        mealCategories = set([meal.category for meal in meals])
        return Response(RestaurantCategoryMealsSerializer(mealCategories, many=True, context={'request': request, 'restaurantId': id}).data)
    except Restaurant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def addMealToRestaurant(request, restaurantId):
    data = request.data

    addMealForm = dict(ChainMap(data, {'restaurant': restaurantId}))
    addMealSerializer = MealSerializer(data=addMealForm)
    if (addMealSerializer.is_valid()):
        addMealSerializer.save()
        return Response(status=status.HTTP_201_CREATED, data=True)
    return Response(status=status.HTTP_400_BAD_REQUEST, data=addMealSerializer.errors)
