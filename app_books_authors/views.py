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
            'user': currentUser,
            'books': Book.objects.all(),
        }
    return render(request, 'books.html', context)

def addBook(request):
    title = request.POST['title']
    description = request.POST['description']
    uploaded_by = User.objects.get(id=request.session['userid'])
    book = Book.objects.create(title=title, description=description, uploaded_by=uploaded_by)
    book.save()
    # After user creates a book, automatically add it to their list of liked books
    getLastBook = Book.objects.last()
    uploaded_by.liked_books.add(getLastBook)
    return redirect('/books')