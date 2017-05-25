from __future__ import unicode_literals

from django.db import models
# from ..first_app.models import Book

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

# one to one relationship
class Description(models.Model):
    content = models.TextField()
    author = models.OneToOneField(Author, related_name = 'authors_desc')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

# many to many relationship
