from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^add_publisher$', views.add_publisher, name = 'add_publisher'),
    url(r'^add_book_to_publisher$', views.add_book_to_publisher, name= 'add_book_to_publisher')
]
