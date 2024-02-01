from random import choices
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.models import FoodieUser, Meal, MealRating, Restaurant
from rest_framework import status

from api.serializers import MealRatingSerializer, MealSerializer, MealWithUserSerializer


@api_view(['POST'])
def rateMeal(request):
    data = request.data
    mealId = data.get('mealId')
    userId = data.get('userId')
    rating = data.get('rating')
    if (mealId is None or userId is None or rating is None):
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Missing Body Args")
    try:
        rating = int(rating)
        if (rating > 5 or rating < 0):
            raise ValueError
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Invalid Rating")
    try:
        user = FoodieUser.objects.get(id=userId)
    except FoodieUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data="User Not Found")
    try:
        meal = Meal.objects.get(id=mealId)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data="Meal Not Found")
    data = {
        'meal': mealId,
        'user': userId,
        'rating': rating
    }
    oldRating = MealRating.objects.filter(
        user=userId, meal=mealId).first()
    if (oldRating is None):
        mealRatingSerializer = MealRatingSerializer(data=data)
    else:
        if (oldRating.rating == rating):
            return Response(data="Rating did not change", status=status.HTTP_204_NO_CONTENT)
        mealRatingSerializer = MealRatingSerializer(
            instance=oldRating, data=data)
    if mealRatingSerializer.is_valid():
        mealRatingSerializer.save()
        updateMealRating(mealId=mealId)
        return Response(True, status=status.HTTP_200_OK)

    return Response(mealRatingSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


def updateMealRating(mealId):
    meal = Meal.objects.get(id=mealId)
    mealRatingsObjects = MealRating.objects.filter(meal=mealId)
    mealRatings = [rating.rating for rating in mealRatingsObjects]
    newRating = sum(mealRatings) / len(mealRatings)
    Meal.objects.filter(id=mealId).update(rating=newRating)


@api_view(['POST'])
def addPromotionToMeal(request, mealId):
    promotionPrice = request.data.get('promotionPrice')
    try:
        promotionPrice = int(promotionPrice)
        if (promotionPrice == 0):
            raise ValueError
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Please enter a valid promotion price')
    try:
        Meal.objects.get(id=mealId)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Meal not found')

    Meal.objects.filter(id=mealId).update(discountedPrice=promotionPrice)
    return Response(status=status.HTTP_200_OK, data=True)


@api_view(['POST'])
def removeMealPromotion(request, mealId):
    try:
        Meal.objects.get(id=mealId)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Meal not found')

    Meal.objects.filter(id=mealId).update(discountedPrice=None)
    return Response(status=status.HTTP_200_OK, data=True)


@api_view(['GET'])
def getMealDetails(request, mealId):
    userId = request.GET.get('userId')
    try:
        meal = Meal.objects.get(id=mealId)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Meal not found')

    if (userId == None):
        return Response(MealSerializer(meal, context={'request': request}).data)

    return Response(MealWithUserSerializer(meal, context={
        'request': request,
        'userId': userId
    }).data)
