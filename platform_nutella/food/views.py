from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import models
from django.contrib.auth import logout
from django.conf.urls import url
from django.conf import settings
from django.shortcuts import redirect
import django.contrib.messages

from .api_openfoodfact import DataApi
from .models import Food, FoodSubstitute, FoodsSaved


def index(request):
    """receives "true" when data bar searches for and displays index"""
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        return redirect('food:research')

    return render(request, 'food/index.html')


def research(request):
    """receives data entered by the user and displays the substitutes"""
    Food.objects.all().delete()

    food_choose = request.POST.get("food_research")

    data_api_openfoodfact = DataApi(food_choose)
    data_products_category = data_api_openfoodfact.select_key_test()

    name_food_nutriscore = data_api_openfoodfact.get_nutriscore_food_choose()
    name_food = Food(name=food_choose, nutriscore=name_food_nutriscore)
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

    if name_food.nutriscore == "e":
        foods_substitutes = FoodSubstitute.objects.exclude(nutriscore="e")
    if name_food.nutriscore == "d":
        foods_substitutes = FoodSubstitute.objects.exclude(nutriscore="e").exclude(nutriscore="d")
    if name_food.nutriscore == "c":
        foods_substitutes = FoodSubstitute.objects.exclude(nutriscore="e").exclude(nutriscore="d").exclude("c")
    if name_food.nutriscore == "b":
        foods_substitutes = FoodSubstitute.objects.exclude(nutriscore="e").exclude(nutriscore="d").exclude("c").exclude("b")
    if name_food.nutriscore == "a":
        foods_substitutes = FoodSubstitute.objects.filter(nutriscore="a")

    context = {
        'foods_substitutes': foods_substitutes,
        'name_food': name_food
    }

    return render(request, 'food/research.html', context)


def save_food(request):
    """save the products choose when the user is logged in"""
    if request.method == 'POST' and request.user.is_authenticated:
        # create a form instance and populate it with data from the request:
        food_substitute_id = request.POST.get("food_substitute_pk")
        current_user = request.user

        food_substitute_choose = FoodSubstitute.objects.get(
            pk=int(food_substitute_id))

        food_substitute_choose_save = FoodsSaved(
            name=food_substitute_choose.name,
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
        messages.success(request, "Produit sauvegardé")

    elif request.method == 'POST' and not request.user.is_authenticated:
        messages.error(request, "Vous ne pouvez pas sauvegarder de produits "
                                  "avant de vous connecter")
        return redirect('accounts:login_page')

    return redirect('food:index')


def details_food(request, product_id):
    """display the details of the substitute"""
    food_detail = get_object_or_404(FoodSubstitute, pk=int(product_id))

    context = {
        'food_detail': food_detail
    }

    return render(request, 'food/details.html', context)


def details_food_saved(request, product_id):
    """display the details of the save substitute"""
    food_detail = get_object_or_404(FoodsSaved, pk=int(product_id))

    context = {
        'food_detail': food_detail
    }

    return render(request, 'food/details.html', context)


def substitutes_saved_user(request):
    """displays the substitutes saved by the user"""
    if request.user.is_authenticated:
        current_user = request.user
        substitutes_saved = FoodsSaved.objects.filter(user=current_user)

        context = {
            'substitutes_saved': substitutes_saved
        }

        return render(request, 'food/substitutes_saved_user.html', context)

    elif not request.user.is_authenticated:
        messages.error(request, "Vous ne pouvez accéder à la page"
                                " 'mes aliments' car vous n'êtes pas connecté")
        return redirect('accounts:login_page')


def contact(request):
    return render(request, 'food/index.html')


def legal_notice(request):
    return render(request, 'food/legal_notice.html')