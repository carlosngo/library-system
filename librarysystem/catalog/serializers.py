from rest_framework import serializers
from .models import Book, BookInstance, Author, Publisher

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=('id', 'name', 'author', 'publish_date', 'review', 'isbn', 'callnumber')

class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookInstance
        fields=('id', 'status')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=('id', 'first_name','last_name', 'date_of_birth', 'date_of_death')

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Publisher
        fields=('id', 'name')