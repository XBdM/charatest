from django.contrib import admin

# Register your models here.

from .models import *#Author, Book, Genre, BookInstance, Project, TeamMember, Repository

#admin.site.register(Book)

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

admin.site.register(Genre)
#admin.site.register(BookInstance)

# Register the Admin classes for Book using the decorator

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
	
    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower',)
        }),
    )
admin.site.register(Project)
admin.site.register(TeamMember)
admin.site.register(Repository)
admin.site.register(Chapter)
admin.site.register(Volume)
admin.site.register(Article)
