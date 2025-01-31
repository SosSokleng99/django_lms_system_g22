from django.contrib import admin

# Register your models here.
from .models import Book, Genre, BookInstance


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'displayGenre')

    list_filter = ('title', 'isbn')


admin.site.register(Book, BookAdmin)



# admin.site.register(Book)
admin.site.register(Genre)

admin.site.register(BookInstance)
