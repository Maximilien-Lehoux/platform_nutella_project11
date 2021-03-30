from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.db import models
from django.contrib.auth import logout
from django.conf.urls import url
from django.conf import settings
from django.shortcuts import redirect


from .api_openfoodfact import DataApi
from .models import Food, FoodSubstitute, FoodsSaved
from .form_food import ResearchFood


def index(request):

    form = ResearchFood()

    return render(request, 'food/index.html', {'form': form})


def research(request):
    # logout(request)

    Food.objects.all().delete()
    # Food.objects.all()


    food_choose = "Cassoulet"

    data_api_openfoodfact = DataApi(food_choose)
    data_products_category = data_api_openfoodfact.select_key_test()

    name_food = Food(name=food_choose)
    name_food.save()

    for data_product_category in data_products_category:
        name = (data_product_category[0])
        image = (data_product_category[1])
        nutriscore = (data_product_category[2])
        url = (data_product_category[3])

        food_substitutes = FoodSubstitute(name=name,
                                          image=image,
                                          nutriscore=nutriscore,
                                          url=url,
                                          food_id=name_food.pk)
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
        print(food_substitute_id)
        current_user = request.user
        print(current_user.id)

        food_substitute_choose = FoodSubstitute.objects.get(pk=int(food_substitute_id))
        print(food_substitute_choose.name)

        food_substitute_choose_save = FoodsSaved(name=food_substitute_choose.name,
                                                 image=food_substitute_choose.image,
                                                 nutriscore=food_substitute_choose.nutriscore,
                                                 url=food_substitute_choose.url,
                                                 user_id=current_user.id)
        food_substitute_choose_save.save()

    elif request.method == 'POST' and not request.user.is_authenticated:
        print("tu n'es pas authentifié)")
        return redirect('accounts:login_page')

    return redirect('food:research')

def select_food(request):
    if request.method == 'POST':
        form = ResearchFood(request.POST)
        # create a form instance and populate it with data from the request:
        if form.is_valid():
            test_food_choose = request.POST.get("research_food")
            print(test_food_choose)

    else:
        form = ResearchFood()

    return render(request, 'food/index.html', {'form': form})




