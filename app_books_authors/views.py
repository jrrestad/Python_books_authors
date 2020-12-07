from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.

def index(request):
    if not 'userId' in request.session:
        return redirect('/')
    else:
        currentUser = User.objects.get(id=request.session['userId'])
        context = {
            'currentUser': currentUser,
        }
    return render(request, 'books.html', context)