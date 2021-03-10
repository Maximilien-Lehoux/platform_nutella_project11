from django.shortcuts import render
from django.db import models


from .api_openfoodfact import DataApi
from .models import Food, FoodSubstitute


def index(request):
    return render(request, 'food/index.html')


def research(request):

    Food.objects.filter(name="cassoulets").delete()
    Food.objects.all()

    food_choose = "cassoulets"

    data_api_openfoodfact = DataApi(food_choose)
    data_products_category = data_api_openfoodfact.select_key_test()
    print(data_products_category)

    name_food = Food(name=food_choose)
    name_food.save()

    for data_product_category in data_products_category:
        name = (data_product_category[0])
        image = (data_product_category[1])
        nutriscore = (data_product_category[2])
        url = (data_product_category[3])

        food_substitutes = FoodSubstitute(name=name, image=image, nutriscore=nutriscore, url=url, food_id=name_food.pk)
        food_substitutes.save()

    foods_substitutes = FoodSubstitute.objects.all()

    context = {
        'foods_substitutes': foods_substitutes
    }

    return render(request, 'food/research.html', context)

