from __future__ import unicode_literals

from django.db import models
from ..author_app.models import Author

# Create your models here.

class BookManager(models.Manager):
    def validate_book(self, postData):
        print postData

        errors = []

        if len(postData['title']) < 2:
            errors.append('title is too short')
        # if len(postData['author']) < 2:
        #     errors.append('author is too short')

        response_to_views = {}

        if errors:
            # failed validations
            response_to_views['status'] = False
            response_to_views['errors'] = errors
            # send messge to views
        else:
            # passed validations
            # create the book
            author = Author.objects.get(id=postData['author_id'])
            book = self.create(title = postData['title'], author = author)
            response_to_views['status'] = True
            response_to_views['book'] = book

        return response_to_views

class Book(models.Model):
    author = models.ForeignKey(Author, related_name = 'wrote_by')
    title = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = BookManager()

class Publisher(models.Model):
    name = models.CharField(max_length = 45)
    books = models.ManyToManyField(Book, related_name = 'published_by')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
