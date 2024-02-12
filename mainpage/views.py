from django.shortcuts import render, HttpResponse
from django.http import JsonResponse


# Create your views here.
def homepage(request):
    return render(request, "mainpage.html")

