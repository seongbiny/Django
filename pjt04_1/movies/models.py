from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    posterpath = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.title