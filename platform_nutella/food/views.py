from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.db import models
from django.contrib.auth import logout
from django.conf.urls import url
from django.conf import settings
from django.shortcuts import redirect


from .api_openfoodfact import DataApi
from .models import Food, FoodSubstitute, FoodsSaved


def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        return redirect('food:research')

    return render(request, 'food/index.html')


def research(request):
    # logout(request)

    Food.objects.all().delete()
    # Food.objects.all()

    food_choose = request.POST.get("food_research")

    data_api_openfoodfact = DataApi(food_choose)
    data_products_category = data_api_openfoodfact.select_key_test()

    name_food = Food(name=food_choose)
    name_food.save()

    for data_product_category in data_products_category:
        name = (data_product_category[0])
        image = (data_product_category[1])
        nutriscore = (data_product_category[2])
        url = (data_product_category[3])
        fat = (data_product_category[4])
        fat_saturated = (data_product_category[5])
        sugar = (data_product_category[6])
        salt = (data_product_category[7])

        food_substitutes = FoodSubstitute(name=name,
                                          image=image,
                                          nutriscore=nutriscore,
                                          url=url,
                                          food_id=name_food.pk,
                                          nutriments_fat=fat,
                                          nutriments_fat_saturated=fat_saturated,
                                          nutriments_salt=salt,
                                          nutriments_sugars=sugar)
        food_substitutes.save()

    foods_substitutes = FoodSubstitute.objects.filter(nutriscore="a")

    context = {
        'foods_substitutes': foods_substitutes
    }

    return render(request, 'food/research.html', context)

# env\Scripts\activate.bat


def save_food(request):
    if request.method == 'POST' and request.user.is_authenticated:
        # create a form instance and populate it with data from the request:
        food_substitute_id = request.POST.get("food_substitute_pk")
        current_user = request.user

        food_substitute_choose = FoodSubstitute.objects.get(pk=int(food_substitute_id))

        food_substitute_choose_save = FoodsSaved(name=food_substitute_choose.name,
                                                 image=food_substitute_choose.image,
                                                 nutriscore=food_substitute_choose.nutriscore,
                                                 url=food_substitute_choose.url,
                                                 user_id=current_user.id,
                                                 nutriments_fat=food_substitute_choose.nutriments_fat,
                                                 nutriments_fat_saturated=food_substitute_choose.nutriments_fat_saturated,
                                                 nutriments_salt=food_substitute_choose.nutriments_salt,
                                                 nutriments_sugars=food_substitute_choose.nutriments_sugars
                                                 )
        food_substitute_choose_save.save()

    elif request.method == 'POST' and not request.user.is_authenticated:
        return redirect('accounts:login_page')

    return redirect('food:index')


def details_food(request, product_id):
    food_detail = FoodSubstitute.objects.get(pk=int(product_id))

    context = {
        'food_detail': food_detail
    }

    return render(request, 'food/details.html', context)


def details_food_saved(request, product_id):
    food_detail = FoodsSaved.objects.get(pk=int(product_id))

    context = {
            'food_detail': food_detail
    }

    return render(request, 'food/details.html', context)


def substitutes_saved_user(request):
    if request.user.is_authenticated:
        current_user = request.user
        substitutes_saved = FoodsSaved.objects.filter(user=current_user)

        context = {
            'substitutes_saved': substitutes_saved
        }

        return render(request, 'food/substitutes_saved_user.html', context)

    elif not request.user.is_authenticated:
        return redirect('accounts:login_page')




