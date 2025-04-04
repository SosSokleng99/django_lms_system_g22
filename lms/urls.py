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

]

#URL: for BookInstance Model 
urlpatterns += [
    path("books_copies", views.BookInstanceListView.as_view(), name="book-copies"),

    # url-path to list all the borrowed books by specific login user.
    path("mybooks/", views.BorrowedBooksByUserListView.as_view(), name="mybooks"),

    #URL - Path to list all borrowed books only for Staff login.
    path("all-borrowed", views.BorrowedAllBooksListView.as_view(), name="all-borrowed")
]

#URL: for Auhtor Model
urlpatterns +=[

    #URL Read: List and DetailView
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>',
         views.AuthorDetailView.as_view(), name='author-detail'),

    #URL Create:
    path('author/create', views.AuthorCreateView.as_view(), name="author-create"),

    #URL Uddate:
    path('author/<int:pk>/update', views.AuthorUpdateView.as_view(), name="author-update"),

    #URL Delete:
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name="author-delete")
]

#URL: for BookInstance Model -- Renew Due_Back date
urlpatterns += [
    path('book-instance/<uuid:pk>/rewnew-date/', views.renew_user_book_due_back_date, name = "renew-user-book-due-back-date")
]

#URL: for BookInstance Model -- Renew Due_Back date
urlpatterns += [
    path('book-instance-recreate/<uuid:pk>/rewnew-date/', views.renew_user_book_due_back_date_recreate, name = "renew-user-book-due-back-date-recreate")
]

#URL: Book Search
urlpatterns += [
    path("search/", views.search_book, name='book-search')
]

