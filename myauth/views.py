from django.shortcuts import render, HttpResponse, redirect
from .models import Users
from django.contrib import messages
from django.contrib.sessions.models import Session
import bcrypt

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
            messages.error(request, "Invalid username")
            return redirect('login')

        if verify_password(password, user.password)==False:
            messages.error(request, "Invalid password")
            return redirect('login')

        messages.success(request, "Login successful")
        request.session['username'] = username
        return redirect('homepage')

    return render(request, "login.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if Users.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            return redirect('signup')

        hashed_password = hash_password(password)

        user = Users(username=username, password=hashed_password)
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, "signup.html")

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password, hashed_password):
    # Verify password
    if bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')):
        return True
    return False