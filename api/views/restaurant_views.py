from random import choices
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import Restaurant
from api.serializers import RestaurantSerializer


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
