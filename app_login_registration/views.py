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
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(firstName=firstName, lastName=lastName, email=email, password=pwHash)
        request.session['userid'] = user.id
        return redirect('/books')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)
    errors = User.objects.validatorLogin(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    elif user:
        loggedUser = user[0]
        if bcrypt.checkpw(password.encode(), loggedUser.password.encode()):
            request.session['userid'] = loggedUser.id
            return redirect('/books')
        else:
            messages.error(request, "Email or password was invalid")
    return redirect('/')

def endSession(request):
    del request.session['userid']
    return redirect('/')