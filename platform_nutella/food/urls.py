from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^research/$', views.research, name="research"),
    # url(r'^$', views.index), # "/store" will call the method "index" in "views.py"
]

app_name = 'food'