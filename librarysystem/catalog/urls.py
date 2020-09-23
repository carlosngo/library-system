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
    path('books/search', views.search, name='searchBook'),
    path('books/review/', views.addReview, name='addReview'),
    path('books/addCopy/', views.addCopy, name='addCopy'),
    path('books/deleteCopy/', views.deleteCopy, name='deleteCopy'),
    path('books/borrowCopy/', views.borrowCopy, name='borrowCopy'),
    path('books/returnCopy/', views.returnCopy, name='returnCopy'),
    
    
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('books/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('registerManager/', views.registerManager, name='registerManager'),
    path('viewLogs/', views.LogListView.as_view(), name='view_logs')
]