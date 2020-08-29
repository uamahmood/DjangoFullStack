from __future__ import unicode_literals
from django.db import models

class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        print(postData)
        if len(postData['title']) < 2:
            errors['title'] = "Title needs to be at least 2 characters"
        if len(postData['network']) < 3:
            errors['network'] = 'Network needs to be at least 3 characters'
        if len(postData['release_date']) < 8:
            errors['release_date'] = "Complete the release date field"
        if len(postData['description']) < 10:
            errors['description'] = "Description needs to be at least 10 characters"
        return errors

class Show(models.Model):
    title = models.CharField(default="Title*", max_length=255)
    network = models.CharField(default="Network*", max_length=255)
    release_date = models.DateField()
    description = models.TextField(default="Description*")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()

    def __repr__(self):
        return f"Show ID: ({self.id})| Title: {self.title}| Network: {self.network}| Release Date: {self.release_date}| Description: {self.description} ||"
