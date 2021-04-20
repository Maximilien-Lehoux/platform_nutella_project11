from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login_page, name="login_page"),
    url(r'^register/$', views.register, name="register"),
    url(r'^connection_user/$', views.connection_user, name="connection_user"),
    url(r'^disconnection_user/$', views.disconnection_user,
        name="disconnection_user"),
    url(r'^change_infos_user/$', views.change_infos_user,
        name="change_infos_user"),
]

app_name = 'accounts'
