from django.db import models

# Create your models here.
class Show(models.Model):
    title = models.CharField(default="Title*", max_length=255)
    network = models.CharField(default="Network*", max_length=255)
    release_date = models.DateField()
    description = models.TextField(default="Description*")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"Show ID: ({self.id})| Title: {self.title}| Network: {self.network}| Release Date: {self.release_date}| Description: {self.description} ||"
