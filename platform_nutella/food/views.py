from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.db import models
from django.contrib.auth import logout
from django.conf.urls import url
from django.conf import settings
from django.shortcuts import redirect


from .api_openfoodfact import DataApi
from .models import Food, FoodSubstitute


def index(request):
    return render(request, 'food/index.html')


def research(request):
    logout(request)

    Food.objects.filter(name="cassoulet").delete()
    Food.objects.all()

    food_choose = "cassoulet"

    data_api_openfoodfact = DataApi(food_choose)
    data_products_category = data_api_openfoodfact.select_key_test()

    name_food = Food(name=food_choose)
    name_food.save()

    for data_product_category in data_products_category:
        name = (data_product_category[0])
        image = (data_product_category[1])
        nutriscore = (data_product_category[2])
        url = (data_product_category[3])

        food_substitutes = FoodSubstitute(name=name, image=image, nutriscore=nutriscore, url=url, food_id=name_food.pk)
        food_substitutes.save()

    foods_substitutes = FoodSubstitute.objects.filter(nutriscore="a")

    context = {
        'foods_substitutes': foods_substitutes
    }

    if request.method == 'POST' and request.user.is_authenticated:
        # create a form instance and populate it with data from the request:
        food_substitute_id = request.POST.get("food_substitute_pk")
        print(food_substitute_id)
        current_user = request.user
        print(current_user.id)

    elif request.method == 'POST' and not request.user.is_authenticated:
        return redirect('accounts:login_page')

    return render(request, 'food/research.html', context)

# env\Scripts\activate.bat


