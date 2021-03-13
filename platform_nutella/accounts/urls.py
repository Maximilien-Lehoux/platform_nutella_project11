from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login_page, name="login_page"),
    url(r'^register/$', views.register, name="register"),
]

app_name = 'accounts'