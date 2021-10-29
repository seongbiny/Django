from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=100)
    debut = models.DateField()

    def __str__(self):
        return f'{self.pk}: {self.name}'


class Album(models.Model):
    artists  = models.ManyToManyField(Artist, related_name='albums')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.pk}: {self.name}'


class Track(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    artists = models.ManyToManyField(Artist, related_name='tracks')
    title = models.CharField(max_length=100)
    lyric = models.TextField()
    click = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.pk}: {self.title}'
