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
            fields = ('pk', 'name',)

    class ReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ('pk', 'title',)

    title = serializers.CharField(min_length=2, max_length=100)
    actors = ActorSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    actor_pks = serializers.ListField(write_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'actors', 'reviews', 'actor_pks')