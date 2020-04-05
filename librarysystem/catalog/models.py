from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

import uuid 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    id_number = models.DecimalField(max_digits=15, decimal_places=0, default=0)
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True)
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    callnumber = models.CharField(max_length=3, help_text='3-digit <a href="https://www.library.illinois.edu/infosci/research/guides/dewey>Call Number</a>')
    review = models.TextField(max_length=1000, help_text='Enter a brief review of the book')
    
    
    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     """Returns the url to access a detail record for this book."""
    #     return reverse('book-detail', args=[str(self.id)])


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

class Publisher(models.Model):
    name=models.CharField(max_length=200)
    city_published=models.CharField(max_length=200)
    publish_date=models.DateField(auto_now=False, auto_now_add=False)