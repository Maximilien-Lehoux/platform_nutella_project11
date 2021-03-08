from django.shortcuts import render
from django.http import HttpResponse

from .api_openfoodfact import DataApi


def index(request):
    return render(request, 'food/index.html')


def research(request):
    data_api_openfoodfact = DataApi("cassoulet")
    data_products_category = data_api_openfoodfact.select_key_test()

    context = {
        'data_products_category': data_products_category
    }

    return render(request, 'food/research.html', context)

