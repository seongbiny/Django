from django.db import models

# Create your models here.

class Music(models.Model):
    title = models.CharField(max_length=30)
    lyrics = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title  