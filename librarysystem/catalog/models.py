from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid 

# Create your models here.

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text='Unique ID for this particular book across whole library')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    name = models.CharField('Name', max_length=200)
    author = models.CharField('Author', max_length=200)
    publisher = models.CharField('Publisher', max_length=200)
    publish_date = models.DateField('Date Published')
    callnumber = models.CharField('Call Number', max_length=3, help_text='3-digit <a href="https://www.library.illinois.edu/infosci/research/guides/dewey>Call Number</a>')
    
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return "/catalog/books/%s" % self.id


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.CASCADE) 
    due_back = models.DateField(default=None, null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=True)


    LOAN_STATUS = (
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='a', help_text='Book Availability')

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.name})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    reviewer = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True)
    text = models.TextField('Review', max_length=1000, help_text='Enter a brief review of the book', blank=True)

    def __str__(self):
        return self.text