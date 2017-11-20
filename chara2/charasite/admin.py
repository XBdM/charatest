from django.contrib import admin

# Register your models here.

from .models import *

#admin.site.register(Book)

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

admin.site.register(Genre)
admin.site.register(Project)
admin.site.register(TeamMember)
admin.site.register(Repository)
admin.site.register(Personal_repository)
admin.site.register(Chapter)
admin.site.register(Volume)
admin.site.register(Article)
