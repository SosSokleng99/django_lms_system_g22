
from django.shortcuts import render
from .models import Book, BookInstance, Genre #Language #Author --> Remianing Table
from django.views import generic


# Create your views here.

def home(request):

    #To count number of Book(Original)
    num_books = Book.objects.all().count()

    #To count number of BookInstance(Book Copies)
    num_book_copies = BookInstance.objects.all().count()

    #To send Data to HTML 

    playLoads = {
        'numberBooks': num_books,
        'numberBookCopies': num_book_copies
    }

    return render(request, 'home.html', context=playLoads)


class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book

class BookInstanceListView(generic.ListView):
    model = BookInstance

from django.contrib.auth.mixins import LoginRequiredMixin

class BorrowedBooksByUserListView(LoginRequiredMixin ,generic.ListView):
    model = BookInstance
    template_name = "lms/myborrowedbooks.html"

    # Create a function to filter only the Specific Books borrowed by Specific User
    def get_queryset(self):
        return(
            #Object Relation Mapping: to query data 
            BookInstance.objects.filter(borrower=self.request.user)
        )
    