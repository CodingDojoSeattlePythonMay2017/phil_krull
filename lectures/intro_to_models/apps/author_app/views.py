from django.shortcuts import render, redirect
from .models import Author, Description

# Create your views here.
def create(request):
    if request.method == 'POST':
        # should be done in the models Manager
        author = Author.objects.create(name = request.POST['name'])

        Description.objects.create(content = request.POST['content'], author = author)

    return redirect('books:index')
