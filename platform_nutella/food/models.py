from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):
    name = models.CharField(max_length=200)


class FoodSubstitute(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    nutriscore = models.CharField(max_length=200)
    url = models.URLField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE)


class FoodsSaved(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    nutriscore = models.CharField(max_length=200)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

