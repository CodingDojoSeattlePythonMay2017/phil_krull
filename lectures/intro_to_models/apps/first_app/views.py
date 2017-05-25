from django.shortcuts import render, redirect
from .models import Book, Publisher
from ..author_app.models import Author
from django.contrib import messages

# Create your views here.
def index(request):
    context = {
        'all_books': Book.objects.all(),
        'all_authors': Author.objects.all(),
        'all_publishers': Publisher.objects.all()
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

def add_publisher(request):
    # should be done inthe manager
    if request.method =='POST':
        Publisher.objects.create(name = request.POST['name'])

    return redirect('books:index')

def add_book_to_publisher(request):
    # should be done inthe manager
    if request.method =='POST':
        book = Book.objects.get(id = request.POST['book_id'])
        publisher = Publisher.objects.get(id = request.POST['publisher_id'])

        publisher.books.add(book)
        
    return redirect('books:index')
