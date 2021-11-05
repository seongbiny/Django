from rest_framework import serializers
from ..models import Actor, Movie, Review

class MovieListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('pk', 'title',)

class MovieSerializer(serializers.ModelSerializer):

    class ActorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = '__all__'

    class ReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ('id', 'title', 'rank')

    actors = ActorSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'overview', 'release_date', 'actors', 'reviews',)