from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    subscriptionExpirationDate = models.DateField()
    location = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=10, null=True)
    landLine = models.CharField(max_length=7)
    image = models.ImageField(upload_to='restaurants/')

    def __str__(self):
        return self.name


class MealCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField(max_length=30)
    discountedPrice = models.FloatField(
        max_length=30, blank=True, default=None, null=True)
    rating = models.IntegerField()
    ingredients = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(MealCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='meals/')

    def __str__(self):
        return self.restaurant.name + " | " + self.name


class FoodieUser(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=10)

    def __str__(self):
        return self.firstName + " " + self.lastName


class MealRating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(FoodieUser, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return self.user.__str__() + " -> " + self.meal.__str__() + " -> " + str(self.rating)
