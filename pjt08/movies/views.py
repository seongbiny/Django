from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Actor, Movie, Review

from .serializers.actor import ActorListSerializer, ActorSerializer
from .serializers.movie import MovieListSerializer, MovieSerializer
from .serializers.review import TopReviewListSerializer, ReviewSerializer


@api_view(['GET', 'POST'])
def actor_list(request):
    
    def actor_list():
        actors = Actor.objects.all()
        serializer = ActorListSerializer(actors, many=True)
        return Response(serializer.data)

    def create_actor():
        serializer = ActorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    if request.method == 'GET':
        return actor_list()
    elif request.method == 'POST':
        return create_actor()


@api_view(['GET', 'PUT', 'DELETE'])
def actor_detail(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)

    def actor_detail():
        serializer = ActorSerializer(actor)
        return Response(serializer.data)

    def update_actor():
        serializer = ActorSerializer(instance=actor, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete_actor():
        actor.delete()
        return Response(data='delete successfully', status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        return actor_detail()
    elif request.method == 'PUT':
        return update_actor()
    elif request.method == 'DELETE':
        return delete_actor()


@api_view(['GET', 'POST'])
def movie_list(request):

    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MovieSerializer(instance=movie, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(data='delete successfully', status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    serializer = TopReviewListSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    
    review = get_object_or_404(Review, pk=review_pk)

    def review_detail():
        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def update_review():
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie)
            return Response(serializer.data)
    
    def delete_review():
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        return review_detail()
    elif request.method == 'PUT':
        return update_review()
    else:
        return delete_review()