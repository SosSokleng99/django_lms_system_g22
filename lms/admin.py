from django.contrib import admin

# Register your models here.
from .models import Book, Genre, BookInstance


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'displayGenre')

    list_filter = ('title', 'isbn')


admin.site.register(Book, BookAdmin)



class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'imprint', 'borrower')

    list_filter = ('borrower', "status")


admin.site.register(BookInstance, BookInstanceAdmin)


# admin.site.register(Book)
admin.site.register(Genre)

