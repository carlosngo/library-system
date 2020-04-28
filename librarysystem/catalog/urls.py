from django.urls import path
from . import views

from django.urls import include
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'), 
    path('author/', views.AuthorListView.as_view(), name='authors'),
    path('search_results/', views.search),
    path('books/<uuid:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<uuid:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('books/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<uuid:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<uuid:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('books/create/', views.AuthorCreate.as_view(), name='book_create'),
    path('books/<uuid:pk>/update/', views.AuthorUpdate.as_view(), name='book_update'),
    path('books/<uuid:pk>/delete/', views.AuthorDelete.as_view(), name='book_delete'),
    path('register/', views.register, name='register'),
    path('registerManager/', views.registerManager, name='registerManager')
]