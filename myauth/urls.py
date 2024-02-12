from django.urls import path
from . import views
from mainpage.views import homepage

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),

    path('user/homepage', homepage, name='homepage')
]