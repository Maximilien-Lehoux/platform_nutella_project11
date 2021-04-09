from django.contrib import admin

from .models import Food, FoodSubstitute, FoodsSaved

admin.site.register(Food)
admin.site.register(FoodSubstitute)
admin.site.register(FoodsSaved)

