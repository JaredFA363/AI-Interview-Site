from django.urls import path
from . import views

urlpatterns = [
    path("homepage", views.homepage, name="homepage"),
    path("custominterviewpage", views.custominterviewpage, name="custominterviewpage"),
    path("logout", views.logout, name="logout"),
    path("yourfeedback", views.yourfeedback, name="yourfeedback"),
]