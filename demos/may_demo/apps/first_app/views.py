from django.shortcuts import render, HttpResponse

# Create your views here.
# this is your controller
def index(request):
    print request.method
    return HttpResponse('response from index the method')
