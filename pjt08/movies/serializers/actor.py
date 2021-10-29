from rest_framework import serializers
from ..models import Actor, Movie

class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name',)

class ActorSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title','overview','release_date','poster_path')
        
    name = serializers.CharField(min_length=1, max_length=100)
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ('id', 'name', 'movies')