import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import FoodieUser, Meal, Restaurant, UserFavoriteMeal
from api.serializers import FoodieUserDisplaySerializer, FoodieUserSerializer, RestaurantFavoriteUserMealsSerializer, UserFavoriteMealSerializer


@api_view(['POST'])
def login(request):
    userName = request.data.get('username')
    password = request.data.get('password')
    try:
        user = FoodieUser.objects.get(username=userName)
        if (user.password == password):
            return Response(FoodieUserDisplaySerializer(user).data)
        else:
            return Response(False)
    except FoodieUser.DoesNotExist:
        return Response(False)


@api_view(['GET'])
def getById(request, id):
    try:
        user = FoodieUser.objects.get(id=id)
    except FoodieUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(FoodieUserDisplaySerializer(user).data)


@api_view(['POST'])
def createAccount(request):
    serializer = FoodieUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(FoodieUserDisplaySerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def toggleFavoriteMeal(request, mealId):
    userId = request.data.get('userId')
    try:
        user = FoodieUser.objects.get(id=userId)
    except FoodieUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data='This user does not exist')
    try:
        meal = Meal.objects.get(id=mealId)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data='This meal does not exist')
    favoriteMeal = UserFavoriteMeal.objects.filter(user=userId, meal=mealId)
    if (len(favoriteMeal) == 0):
        userFavoriteMealSerializer = UserFavoriteMealSerializer(data={
            'user': userId,
            'meal': mealId
        })
        if (userFavoriteMealSerializer.is_valid()):
            userFavoriteMealSerializer.save()
        else:
            return Response(userFavoriteMealSerializer.errors)
    else:
        UserFavoriteMeal.objects.filter(user=userId, meal=mealId).delete()

    return Response(status=status.HTTP_200_OK, data=True)


@api_view(['GET'])
def getUserFavorites(request, userId):
    favorites = UserFavoriteMeal.objects.filter(user=userId)
    restaurantToMealsDict = {}

    for favoriteMeal in favorites:
        meal = favoriteMeal.meal
        restaurant = favoriteMeal.meal.restaurant
        if (restaurant in restaurantToMealsDict):
            restaurantToMealsDict[restaurant].append(meal)
        else:
            restaurantToMealsDict[restaurant] = [meal]

    response = []
    for restaurant, meals in restaurantToMealsDict.items():
        response.append(RestaurantFavoriteUserMealsSerializer(restaurant, context={
                        'request': request, 'meals': meals}).data)

    return Response(response)


@api_view(["GET"])
def getCartItems(request):
    mealIds = request.GET.get('mealIds')
    restaurantId = request.GET.get('restaurantId')
    try:
        restaurantId = int(restaurantId)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Invalid or No restaurant id was provided')
    try:
        mealIds = list(json.loads(mealIds))
        if not isinstance(mealIds, list):
            raise ValueError()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Invalid or No ids were provided')

    restaurant = Restaurant.objects.get(id=restaurantId)
    meals = Meal.objects.filter(id__in=mealIds)
    return Response(RestaurantFavoriteUserMealsSerializer(restaurant, context={
        'request': request, 'meals': meals}).data)
