from django.db import models

# Create your models here.

class Publisher(models.Model):
	name = models.CharField(max_length=200, help_text='Please enter the publisher name.')
	
	def __str__(self):
		return self.name

from django.urls import reverse

class Book(models.Model):
    name = models.CharField('Name', max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True)
    publish_date=models.DateField('Date Published', null=True, blank=True)
    review = models.TextField('Review', max_length=1000, help_text='Enter a brief review of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    callnumber = models.CharField('Call Number', max_length=3, help_text='3-digit <a href="https://www.library.illinois.edu/infosci/research/guides/dewey>Call Number</a>')
    
    
    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     """Returns the url to access a detail record for this book."""
    #     return reverse('book-detail', args=[str(self.id)])

import uuid 

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='a', help_text='Book Availability')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.name})'

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    # def get_absolute_url(self):
    #     return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'