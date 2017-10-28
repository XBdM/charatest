from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
        
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    #avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    email_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Project(models.Model):
    name = models.CharField(max_length=200, help_text="Enter the name of your project")
    date_start = models.DateTimeField(auto_now_add = True)
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
    prevChapter = models.ForeignKey('Chapter', null = True, blank = True, on_delete = models.SET_NULL, help_text="The previous chapter")
    summary = models.TextField(max_length=1000, null = True, blank = True, help_text="Enter a brief summary for this chapter")
    content = models.TextField(max_length=200000, null = True, blank = True, help_text="Your chapter")
    date_of_creation = models.DateTimeField(auto_now_add = True)
    date_of_last_edit = models.DateTimeField(auto_now = True)
    is_published = models.BooleanField(blank=True, default=False)
    
    def get_absolute_url(self):
        return reverse('chapter_detail', args=[str(self.id)])

    def __str__(self):
        return self.title
    
    class Meta:
        
        ordering =['number']
        
class Article(models.Model):
    title = models.CharField(max_length=200, help_text="Enter the title of this article")
    writer = models.ForeignKey(User, on_delete = models.CASCADE)
    prevArticle = models.ForeignKey('Article', null = True, blank = True, on_delete = models.SET_NULL, help_text="The previous article")
    summary = models.TextField(max_length=1000, null = True, blank = True, help_text="Enter a brief summary for this article")
    content = models.TextField(max_length=200000, null = True, blank = True, help_text="Your article")
    date_of_creation = models.DateTimeField(auto_now_add = True)
    date_of_last_edit = models.DateTimeField(auto_now = True)
    is_published = models.BooleanField(blank=True, default=False)
    
    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.title
    
    class Meta:
        
        ordering = ['-date_of_last_edit']


class Volume(models.Model):
    project = models.ForeignKey('Project', on_delete = models.CASCADE)
    number = models.IntegerField(help_text = 'Number of the chapter')
    begin = models.IntegerField(help_text = 'first chap')
    end = models.IntegerField(help_text = 'last chap')
    title = models.CharField(max_length=200, help_text="Enter the title of this volume")


class CommentArticle(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=1000, null=True, blank=True, help_text="Write a comment !")
    date_of_creation = models.DateTimeField(auto_now_add=True)
    date_of_last_edit = models.DateTimeField(auto_now=True)

    nb_upvote = models.IntegerField(default=0)
    nb_downvote = models.IntegerField(default=0)


class CommentChapter(models.Model):
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=1000, null=True, blank=True, help_text="Write a comment !")
    date_of_creation = models.DateTimeField(auto_now_add=True)
    date_of_last_edit = models.DateTimeField(auto_now=True)

    nb_upvote = models.IntegerField(default=0)
    nb_downvote = models.IntegerField(default=0)


class CommentProject(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=1000, null=True, blank=True, help_text="Write a comment !")
    date_of_creation = models.DateTimeField(auto_now_add=True)
    date_of_last_edit = models.DateTimeField(auto_now=True)

    nb_upvote = models.IntegerField(default=0)
    nb_downvote = models.IntegerField(default=0)
