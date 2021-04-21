from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', views.login_page, name="login_page"),
    url(r'^register/$', views.register, name="register"),
    url(r'^connection_user/$', views.connection_user, name="connection_user"),
    url(r'^disconnection_user/$', views.disconnection_user,
        name="disconnection_user"),
    path("password_reset/", views.password_reset_request, name="password_reset"),

]

app_name = 'accounts'
