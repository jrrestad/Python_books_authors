from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'index.html')

def registration(request):
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    email = request.POST['email']
    password = request.POST['password']
    pwHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(pwHash)
    errors = User.objects.validatorRegister(request.POST)
    print(errors.items())
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(firstName=firstName, lastName=lastName, email=email, password=pwHash)
        request.session['userId'] = user.id
        return redirect('/dashboard')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)
    errors = User.objects.validatorLogin(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print("\n*****ERRORS OCCURRED*****\n")
            print("Error: " + value + "\n")
        return redirect('/')
    elif user:
        loggedUser = user[0]
        if bcrypt.checkpw(password.encode(), loggedUser.password.encode()):
            request.session['userId'] = loggedUser.id
            return redirect('/dashboard')
        else:
            messages.error(request, "Email or password was invalid")
    return redirect('/')

def dashboard(request):
    if 'userId' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['userId'])
        }
        return render(request, 'dashboard.html', context)

def endSession(request):
    del request.session['userId']
    return redirect('/')