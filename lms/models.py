import uuid
from django.db import models
from django.urls import reverse

import uuid  # Required for unique book instances
from datetime import date
from django.conf import settings  # Required to assign User as a borrower

# Model: Genre
class Genre(models.Model):

    """Genre of Book: Science, Philosophy etc"""
    #Peroperties / Data
    name = models.CharField(max_length=20, help_text="Enter Book's Genre name.")

    #MetaData Class used to regulate data
    class Meta:
        ordering = ['name']
    
    
    #Functions / Method
    def __str__(self):
        '''
        String for representing the Genre model object.
        '''
        return self.name
    
    #
    def get_absolute_url(self):
        '''
        Return a specific detail data of Genre model based on id.
        '''
        return reverse("genre-detail", kwargs={"pk": self.pk})
    

# Model: Books
class Book(models.Model):

    #Book Data field / Properties
    title = models.CharField(max_length=200)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # Foreign Key used because book can only have one author, but authors can have multiple books.

    #Metadata
    class Meta:
        ordering = ['-title'] #Ensure the Title when display on HTML it ordered from Z-A
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.pk})

    def displayGenre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        genres = self.genre.all()  # Retrieve all genres associated with the book instance
        genre_names = [genre.name for genre in genres]  # Create a list of genre names
        return ', '.join(genre_names)  # Join the list into a single string separated by commas

    displayGenre.short_description = 'Genre'



class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability')


    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date. Return True or False based date.today() > due_back"""
        return bool(date.today() > self.due_back)

    #Metadata
    class Meta:
        ordering = ['due_back']
    
    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('bookinstance-detail', kwargs={"pk": self.pk})
    

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

