from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render
from catalog.models import Author
from django.contrib.auth.forms import UserCreationForm
from catalog.models import Book, Author, BookInstance, Profile, User

import datetime

# Create your views here.
from catalog.models import Book, Author, BookInstance, Publisher

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'book_list'
    template_name = 'books.html'

def search(request):
    # query = self.request.GET.get('search-bar')
    # object_list = Book.objects.filter(Q(name__icontains=query))
    # # return object_list
    error = False
    if 'search-bar' in request.GET and request.GET['search-bar']:
        search = request.GET['search-bar']
        if not search:
            error = True
        else:
            books = Book.objects.filter(name__icontains=search)
            return render(request, 'search_results.html', {'books': books, 'query':search})
        return render(request, 'Books.html', {'error': error})
        
class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book_details'
    template_name = 'book_details.html'

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


def index(request):

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0) # Number of visits to this view, as counted in the session variable.s

    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed') )

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

def book_details(request):
    return BookDetailView.as_view()

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = ['name', 'author', 'publisher', 'publish_date', 'review', 'isbn', 'callnumber']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from catalog.models import Book, Author, BookInstance
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.http import HttpResponse
    
def profile(request):
  return render(request, 'profile.html', {})


def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.profile.id_number = form.cleaned_data.get('id_number')
        user.save()
        users = Group.objects.get(name='Users') 
        users.user_set.add(user)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(request=request, username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'register.html', {'form': form})

def registerManager(request):
    form = RegisterForm(request.POST)

    current_user = request.user
    if current_user.is_authenticated == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if current_user.groups.filter(name='Administrators').exists() == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.profile.id_number = form.cleaned_data.get('id_number')
        user.save()
        managers = Group.objects.get(name='Managers') 
        managers.user_set.add(user)
        return redirect('/')
    return render(request, 'register_manager.html', {'form': form})