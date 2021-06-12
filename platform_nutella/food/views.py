from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import models
from django.contrib.auth import logout
from django.conf.urls import url
from django.conf import settings
from django.shortcuts import redirect
import django.contrib.messages


from .models import Food, FoodSubstitute, FoodsSaved
from .manager import ResearchFood, DatabaseSaveFood


def index(request):
    """receives "true" when data bar searches for and displays index"""
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        return redirect('food:research')

    return render(request, 'food/index.html')


def research(request):
    """receives data entered by the user and displays the substitutes"""
    research_food = ResearchFood()
    # If count database > 1000
    research_food.delete_database()

    food_choose = request.POST.get("food_research")

    context = research_food.get_context_food(food_choose)

    return render(request, 'food/research.html', context)


def save_food(request):
    """save the products choose when the user is logged in"""
    if request.method == 'POST' and request.user.is_authenticated:
        # create a form instance and populate it with data from the request:
        food_substitute_id = request.POST.get("food_substitute_pk")
        current_user = request.user

        food_substitute_choose = FoodSubstitute.objects.get(
            pk=int(food_substitute_id))

        database_save_food = DatabaseSaveFood()

        database_save_food.save_food(
            food_substitute_choose, current_user
        )

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