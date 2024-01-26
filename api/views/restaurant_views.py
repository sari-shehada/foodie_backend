from random import choices
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
    return Response(RestaurantSerializer(user).data)


@api_view(['GET'])
def getDisplayRestaurants(request):
    ids = Restaurant.objects.values_list('pk', flat=True)
    selectedIds = choices(ids, k=5)
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
