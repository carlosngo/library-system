import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from catalog.models import BookInstance, Book
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        # PAST check 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # RANGE check (only up to 4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data

class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']
       
       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))

       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

       return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')} 

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    username = forms.CharField(max_length=30, help_text='Username')
    email = forms.EmailField(max_length=200, help_text='Email Address')
    id_number = forms.DecimalField(max_digits=15, decimal_places=0)

    class Meta:
        model = User
        fields = ('id_number', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('isbn', 'name', 'author', 'publisher', 'publish_date', 'callnumber')

class BookInstanceForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ('book', 'due_back', 'borrower', 'status')