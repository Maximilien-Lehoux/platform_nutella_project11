from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):
    """creation of the selected food table"""
    name = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=200, null=True, blank=True)


class FoodSubstitute(models.Model):
    """creation of the food subtitus table"""
    name = models.CharField(max_length=200)
    image = models.URLField()
    nutriscore = models.CharField(max_length=200)
    url = models.URLField()
    nutriments_fat = models.CharField(max_length=200, null=True, blank=True)
    nutriments_fat_saturated = models.CharField(max_length=200, null=True, blank=True)
    nutriments_sugars = models.CharField(max_length=200, null=True, blank=True)
    nutriments_salt = models.CharField(max_length=200, null=True, blank=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)


class FoodsSaved(models.Model):
    """products saved table creation"""
    name = models.CharField(max_length=200)
    image = models.URLField()
    nutriscore = models.CharField(max_length=200)
    url = models.URLField()
    nutriments_fat = models.CharField(max_length=200, null=True, blank=True)
    nutriments_fat_saturated = models.CharField(max_length=200, null=True, blank=True)
    nutriments_sugars = models.CharField(max_length=200, null=True, blank=True)
    nutriments_salt = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

