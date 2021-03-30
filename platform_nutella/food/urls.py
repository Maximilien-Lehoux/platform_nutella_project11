from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^research/$', views.research, name="research"),
    url(r'^save_food/$', views.save_food, name="save_food"),
    url(r'^select_food/$', views.select_food, name="select_food"),
    # url(r'^$', views.index), # "/store" will call the method "index" in "views.py"
]

app_name = 'food'