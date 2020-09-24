from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group

from django.contrib.admin.models import LogEntry

from django.urls import reverse
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect, HttpResponse

from catalog.models import Book, BookInstance, Profile, User, Review
from catalog.forms import RenewBookForm, RegisterForm, BookForm, BookInstanceForm
    
import datetime

# Create your views here.

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
    if 'query' in request.GET and request.GET['query']:
        search = request.GET['query']
        if not search:
            error = True
        else:
            books = Book.objects.filter(name__icontains=search)
            return render(request, 'books.html', {'book_list': books, 'query':search})
        return render(request, 'Books.html', {'error': error})
        
class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_details.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['book_details'] = context['book']
        context['book_copies'] = BookInstance.objects.filter(book__id=context['book'].id)
        context['available_book_copies'] = BookInstance.objects.filter(book__id=context['book'].id, status='a')
        context['reserved_book_copies'] = BookInstance.objects.filter(book__id=context['book'].id, status='r')
        context['book_reviews'] = Review.objects.filter(book__id=context['book'].id)
        print(context)
        # Add in a QuerySet of all the books
        # context['book_details'] = Book.objects.all()
        # context
        return context

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
    num_visits = request.session.get('num_visits', 0) # Number of visits to this view, as counted in the session variable.s

    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
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

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = ['name', 'author', 'publisher', 'publish_date', 'review', 'isbn', 'callnumber']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

class LogListView(generic.ListView):
  model = LogEntry
  context_object_name = 'log_list'
  template_name = 'logs.html'

def profile(request):
    current_user = request.user
    if current_user.groups.filter(name='Users').exists() == True:
        books = BookInstance.objects.filter(borrower=current_user)
        reviews = Review.objects.filter(reviewer=current_user.profile)
        return render(request, 'profile.html', {'my_books': books, 'my_reviews': reviews})
    return render(request, 'profile.html', {})

def register(request):
    if request.method == 'POST':
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
        else:
            return render(request, 'register.html', {'form': form})        
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def registerManager(request):
    current_user = request.user
    if current_user.is_authenticated == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if current_user.groups.filter(name='Administrators').exists() == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if request.method == 'POST':
        form = RegisterForm(request.POST)
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
        else:
            return render(request, 'register_manager.html', {'form': form})
    form = RegisterForm()
    return render(request, 'register_manager.html', {'form': form})


def addBook(request):
    current_user = request.user
    if current_user.is_authenticated == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if current_user.groups.filter(name='Managers').exists() == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            print(book)
            book.save()
            return redirect('/catalog/books/')
        else:
            return render(request, 'add_book.html', {'form': form})
    form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def deleteBook(request):

    current_user = request.user
    if current_user.is_authenticated == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if current_user.groups.filter(name='Managers').exists() == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    Book.objects.filter(id=request.POST.get("book-id", "")).delete()
    return redirect('/catalog/books')

def updateBook(request):
    current_user = request.user
    if current_user.is_authenticated == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if current_user.groups.filter(name='Managers').exists() == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    
    if request.method == 'POST':
        book = Book.objects.get(id=request.POST.get("book-id", ""))
        form = BookForm(request.POST)
        if form.is_valid():
            updated_book = form.save(commit=False)
            book.isbn = updated_book.isbn
            book.name = updated_book.name
            book.author = updated_book.author
            book.publisher = updated_book.publisher
            book.publish_date = updated_book.publish_date
            book.callnumber = updated_book.callnumber
            book.save()
            return redirect(f'/catalog/books/{book.id}')
        else:
            return render(request, 'update_book.html', {'form': form, 'bookId': book.id})
    book = Book.objects.get(id=request.GET.get('book-id', ''))
    form = BookForm(instance=book)
    return render(request, 'update_book.html', {'form': form, 'bookId': book.id})

def addReview(request):
    current_user = request.user
    if current_user.is_authenticated == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if current_user.groups.filter(name='Users').exists() == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    book = Book.objects.get(id=request.POST.get("book-id", ""))
    text = request.POST.get("review", "")
    review = Review(book=book, reviewer=current_user.profile, text=text)
    review.save()
    return redirect(f'/catalog/books/{book.id}')

def addCopy(request):
    current_user = request.user
    if current_user.is_authenticated == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if current_user.groups.filter(name='Managers').exists() == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    book = Book.objects.get(id=request.POST.get("book-id", ""))
    copy = BookInstance(book=book)
    copy.save()
    return redirect(f'/catalog/books/{book.id}')

def deleteCopy(request):
    current_user = request.user
    if current_user.is_authenticated == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if current_user.groups.filter(name='Managers').exists() == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    BookInstance.objects.filter(id=request.POST.get("book-copy-id", "")).delete()
    return redirect(f'/catalog/books/{request.POST.get("book-id", "")}')

def borrowCopy(request):
    current_user = request.user
    if current_user.is_authenticated == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if current_user.groups.filter(name='Users').exists() == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    copy = BookInstance.objects.get(id=request.POST.get("book-copy-id", ""))
    copy.borrower = current_user
    copy.status = 'r'
    copy.save()
    return redirect(f'/catalog/books/{request.POST.get("book-id", "")}')

def returnCopy(request):
    current_user = request.user
    if current_user.is_authenticated == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    if current_user.groups.filter(name='Users').exists() == False:
        res = HttpResponse("Unauthorized")
        res.status_code = 401
        return res
    copy = BookInstance.objects.get(id=request.POST.get("book-copy-id", ""))
    copy.borrower = None
    copy.status = 'a'
    copy.save()
    return redirect(request.META['HTTP_REFERER'])
