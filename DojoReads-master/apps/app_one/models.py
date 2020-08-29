from django.db import models
import re
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if len(postData['name'])<1:
            errors['name']="All fields are required"
        # elif str.isalpha(postData["name"])==False:
        #     errors['name']="Name cannot contain numbers"
        if len(postData['alias'])<1:
            errors['alias']="All fields are required"
        elif str.isalpha(postData["alias"])==False:
            errors['alias']="Name cannot contain numbers"
        if len(postData['email'])<1:
            errors['email']="All fields are required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email']="Please enter a valid email"
        elif User.objects.filter(email=postData['email']):
            errors['email']="Enter a unique email"
        if len(postData['pass'])<1:
            errors['pass']="All fields are required"
        elif len(postData['pass'])< 8:
            errors['pass']="Password should be at least eight characters"
        if postData['pass2']!=postData['pass']:
            errors['pass2']="Passwords don't match"
        
        return errors

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors={}
        if len(postData['title'])<1:
            errors['title']="All fields are required"
        return errors
class AuthorManager(models.Manager):
    def author_validator(self, postData):
        errors={}
        return errors
class User(models.Model):
    name=models.CharField(max_length=255)
    alias=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = UserManager()


class Author(models.Model):
    name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = AuthorManager()

class Book(models.Model):
    title=models.CharField(max_length=255)
    author=models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE,)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    review=models.TextField()
    rating=models.IntegerField()
    poster=models.ForeignKey(User, related_name="posters",on_delete=models.CASCADE,)
    subject=models.ForeignKey(Book, related_name="subjects",on_delete=models.CASCADE,)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)