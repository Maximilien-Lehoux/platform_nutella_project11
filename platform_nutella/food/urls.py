from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^research/$', views.research, name="research"),
    url(r'^save_food/$', views.save_food, name="save_food"),
    url(r'^substitutes_saved_user/$', views.substitutes_saved_user,
        name="substitutes_saved_user"),
    path('details_food/<product_id>/', views.details_food, name="details_food"),
    path('details_food_saved/<product_id>/', views.details_food_saved, name="details_food_saved"),
    url(r'^index/$', views.index, name="index"),
]

app_name = 'food'