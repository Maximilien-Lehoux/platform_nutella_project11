from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=200, unique=True)



class FoodSubstitute(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    nutriscore = models.CharField(max_length=200)
    url = models.URLField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
