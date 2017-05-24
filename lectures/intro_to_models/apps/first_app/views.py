from django.shortcuts import render, redirect
from .models import Book
from django.contrib import messages

# Create your views here.
def index(request):
    context = {
        'all_books': Book.objects.all()
    }
    return render(request, 'first_app/index.html', context)


def create(request):
    if request.method == "POST":
        response_from_models = Book.objects.validate_book(request.POST)

        if response_from_models['status']:
            # passed the validations
            # save something in session
            # redirect to a different page
            pass
        else:
            # send a message to the cliend
            for error in response_from_models['errors']:
                messages.error(request, error)

    return redirect('books:index')
