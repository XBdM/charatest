from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
import uuid # Required for unique book instances

class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name
        

class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book_detail', args=[str(self.id)])
        
class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id,self.book.title)
        
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
        
    permissions = (("can_mark_returned", "Set book as returned"),) 
        
class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author_detail', args=[str(self.id)])
    

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)


class Project(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the name of your team")
    date_start = models.DateField(auto_now_add = True)
    description = models.TextField(max_length=1000, null = True, blank = True, help_text="Enter a brief description of the project")
    is_public = models.BooleanField(help_text='Do you want the project to be referenced ?')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    is_published = models.BooleanField(blank = True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])
        
class TeamMember(models.Model):

    member = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Project', on_delete = models.CASCADE)
    
    RANK_STATUS = (
        ('o', 'Owner'),
        ('a', 'Administrator'),
        ('m', 'Moderator'),
        ('w', 'Writer'),
        ('t', 'Translator'),
        ('r', 'Reader'),
    )
    
    role = models.CharField(max_length=1, choices = RANK_STATUS, blank = False, default='a', help_text='Define the level of authorisation for the User')
    date_join = models.DateField(auto_now_add = True)

    def __str__(self):
        return '%s: %s, %s' % (self.team, self.member, self.role)

        
class Repository(models.Model):
    project = models.ForeignKey('Project', on_delete = models.CASCADE)
    parent_repository = models.ForeignKey('self', null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, help_text="Enter the name of your new repository")
    
    def __str__(self):
        return self.name
        
class Chapter(models.Model):
    project = models.ForeignKey('Project', on_delete = models.CASCADE)
    repository = models.ForeignKey('Repository', on_delete = models.CASCADE)
    number = models.IntegerField(help_text = 'Number of the chapter')
    title = models.CharField(max_length=200, help_text="Enter the title of this chapter")
    summary = models.TextField(max_length=1000, null = True, blank = True, help_text="Enter a brief summary for this chapter")
    chapter = models.TextField(max_length=200000, null = True, blank = True, help_text="Your chapter")
    date_of_creation = models.DateField(auto_now_add = True)
    date_of_last_edit = models.DateField(auto_now = True)
    is_published = models.BooleanField(blank=True, default=False)


class Volume(models.Model):
    project = models.ForeignKey('Project', on_delete = models.CASCADE)
    number = models.IntegerField(help_text = 'Number of the chapter')
    begin = models.IntegerField(help_text = 'first chap')
    end = models.IntegerField(help_text = 'last chap')
    title = models.CharField(max_length=200, help_text="Enter the title of this volume")

