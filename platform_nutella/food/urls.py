from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^research/$', views.research, name="research"),
    url(r'^save_food/$', views.save_food, name="save_food"),
    url(r'^index/$', views.index, name="index"), # "/store" will call the method "index" in "views.py"
]

app_name = 'food'