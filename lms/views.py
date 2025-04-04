
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from .models import Book, BookInstance, Genre, Author #Language #Author --> Remianing Table
from django.views import generic

#Import Helper classes for Create, Update and Delete operation
from django.views.generic.edit import CreateView, UpdateView, DeleteView



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

from django.contrib.auth.mixins import PermissionRequiredMixin
'''
PermissionRequiredMixin is a class used to required for a staff account to login in order to see the this particular view.
'''

class BorrowedAllBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'lms.can_views_all_borrowed_books'
    template_name = "lms/bookinstance_list_borrowed_all.html"

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o').order_by('due_back')
        )
    
    
#CRUD operation: Author models
# Read operation: ListView and DetailView
class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author

class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author 


#Create operation: CreateView
class AuthorCreateView(PermissionRequiredMixin, CreateView):
    model = Author
    # fields = '__all__' #Optionals: you can use '__all__' value to be able do Create Operation for all fields.
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': "Filled the Date of Author Death. Leave blank if he/she alives"}
    permission_required = 'lms.add_author'

#Update operation: UpdateView
class AuthorUpdateView(PermissionRequiredMixin, UpdateView):
    model = Author
    fields= '__all__'
    permission_required = 'lms.change_author'

#Delete operation: DeleteView
class AuthorDeleteView(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = 'lms.delete_author'
    success_url = reverse_lazy('authors')

     #To validate that the Author Delete Operation always go success_url which is Author List by default
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )

import datetime
from lms.forms import RenewBookInstanceDate
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('lms.can_views_all_borrowed_books', raise_exception=True)
#Function for handling Book Due Back date
def renew_user_book_due_back_date(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data based on user filled Data in the form
    if request.method == "POST":

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookInstanceDate(request.POST)
        # Check if the form's data is valid:
        if form.is_valid():
           # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
           book_instance.due_back = form.cleaned_data['renewal_date']
           book_instance.save()
           # redirect to the Successful URL
           return HttpResponseRedirect(reverse('all-borrowed'))
        
    #IF user not fill the form, we suggest the Proposed Date for renewal 
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookInstanceDate(initial={'renewal_date': proposed_renewal_date})


    playLoads = {
        'form': form,
        'book_instance': book_instance
        
    }

    return render(request, 'lms/book_instance_renew_date.html', playLoads)


from .forms import RenewBookInstanceDueBackDateRecreate

def renew_user_book_due_back_date_recreate(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":

        form = RenewBookInstanceDueBackDateRecreate(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date_recreate']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    
    else:
        propose_renewal_date = datetime.date.today() + datetime.timedelta(weeks=1)
        form = RenewBookInstanceDueBackDateRecreate(initial={'renewal_date_recreate': propose_renewal_date })

    play_loads = {
        'form': form,
        'book_instance': book_instance
    }

    return render(request, 'lms/renew_book_instance_date_recreate.html', context = play_loads)


from .forms import SearchBook

def search_book(request):


    form = SearchBook(request.GET)
    search_results = []

    if form.is_valid():

        search_query = form.cleaned_data.get('search_query')
        if search_query:
            search_results = Book.objects.filter(title__icontains=search_query) #Search Book Title

    play_loads = {
        'form': form,
        'search_results': search_results
    }

    return render(request, 'lms/book_search_result.html', play_loads)