from django.urls import path
from . import views

from django.urls import include
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    
    path('books/', views.BookListView.as_view(), name='book-list'), 
    path('books/<uuid:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.addBook, name='addBook'),
    path('books/delete/', views.deleteBook, name='deleteBook'),
    path('books/update/', views.updateBook, name='updateBook'),
    path('search_results/', views.search),
    
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('books/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<uuid:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<uuid:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('registerManager/', views.registerManager, name='registerManager'),
    path('viewLogs/', views.LogListView.as_view(), name='view_logs')
]