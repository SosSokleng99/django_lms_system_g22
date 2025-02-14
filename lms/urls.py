from django.urls import path
from . import views

#To defined URL for app
urlpatterns = [
    path('', views.home, name="home"), #Defualt
]

#URL: for BOOK Model
urlpatterns += [
    path("books/", views.BookListView.as_view(), name="books"), #BookListView
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book-detail"),

    # url-path to list all the borrowed books by specific login user.
    path("mybooks/", views.BorrowedBooksByUserListView.as_view(), name="mybooks")

]

#URL: for BookInstance Model 

urlpatterns += [
    path("books_copies", views.BookInstanceListView.as_view(), name="book-copies"),
]

#URL: for Auhtor Model
urlpatterns +=[
    
]

