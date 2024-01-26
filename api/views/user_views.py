from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import FoodieUser
from api.serializers import FoodieUserDisplaySerializer, FoodieUserSerializer


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
