from rest_framework import serializers
from ..models import Actor, Movie, Review

class TopReviewListSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ('pk', 'title',)

    movie = MovieSerializer(many=True)

    class Meta:
        model = Review
        fields = ('pk', 'title', 'movie')

class ReviewSerializer(serializers.ModelSerializer):

    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = '__all__'

    content = serializers.CharField(required=False)
    movie = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ('pk', 'title', 'movie', 'content')

    def create(self, validated_data):
        actor_pks = validated_data.pop('actor_pks')
        review = Review.objects.create(**validated_data)
        for actor_pk in actor_pks:
            review.actors.add(actor_pk)
        return review

    def update(self, review, validated_data):
        actor_pks = validated_data.pop('actor_pks')
        for attr, value in validated_data.items():
            setattr(review, attr, value)
        review.save()

        review.artists.clear()
        for actor_pk in actor_pks:
            review.artists.add(actor_pk)
        return review