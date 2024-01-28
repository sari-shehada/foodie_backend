
import random
from api.models import MealCategory
from rest_framework.decorators import api_view
from random import choices
from rest_framework.response import Response

from api.serializers import MealCategorySerializer


@api_view(['GET'])
def getDisplayCategories(request):
    ids = MealCategory.objects.values_list('pk', flat=True)
    ids = sorted(ids)
    selectedIds = random.sample(ids, k=5 if len(ids) > 5 else len(ids))
    categories = MealCategory.objects.filter(id__in=selectedIds)
    return Response(MealCategorySerializer(categories, context={'request': request}, many=True).data)
