from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

# Create your views here.

def index(request):
    if not 'userid' in request.session:
        return redirect('/')
    else:
        currentUser = User.objects.get(id=request.session['userid'])
        context = {
            'currentUser': currentUser,
            'user': User.objects.get(id=request.session['userid']),
        }
    return render(request, 'books.html', context)