from django.shortcuts import render, HttpResponse, redirect
from .models import Users
from django.contrib import messages
#from mainpage.views import homepage

# Create your views here.
def home(request):
    return render(request, "base.html")

def login(request):
    if request.method == 'POST':    
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            messages.error(request, "Invalid username or password")
            print("i")
            return redirect('login')

        if user.password != password:
            messages.error(request, "Invalid username or password")
            print("u")
            return redirect('login')

        messages.success(request, "Login successful")
        print("y")
        #return redirect('home')
        return redirect('homepage')

    return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            print("x")
            return redirect('signup')

        if Users.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            print("n")
            return redirect('signup')

        user = Users(username=username, password=password)
        user.save()

        messages.success(request, "Account created successfully")
        print("b")
        return redirect('login')

    return render(request, "signup.html")