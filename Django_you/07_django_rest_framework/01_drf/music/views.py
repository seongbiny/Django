
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.shortcuts import render, get_list_or_404, get_object_or_404

from music import serializers
from .models import Artist, Music
from .serializers import MusicListSerializer, MusicSerializer, ArtistListSerializer, ArtistSerializer

# Create your views here.

@api_view(['GET'])
def music_list(request):
    if request.method =='GET':
        music = get_list_or_404(Music)
        serializer = MusicListSerializer(music, many=True)    
        return Response(serializer.data)

    elif request.method =='POST':
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
def music_detail(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)
    
    if request.method =='GET':
        serializer = MusicSerializer(music)    
        return Response(serializer.data)

    elif request.method =='DELETE':
        music.delete()
        data = {
            'delete': f'데이터 {music_pk}번이 삭제되었습니다.'
        }   
        return Response(data, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def artist_list(request):
    if request.method =='GET':
        artist = get_list_or_404(Artist)
        serializer = ArtistListSerializer(artist, many=True)    
        return Response(serializer.data)

    elif request.method =='POST':
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    
    if request.method =='GET':
        serializer = ArtistSerializer(artist)    
        return Response(serializer.data)

    elif request.method =='DELETE':
        artist.delete()
        data = {
            'delete': f'데이터 {artist_pk}번이 삭제되었습니다.'
        }   
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def artist_music(request,artist_pk):
    artist = get_object_or_404(Artist,pk=artist_pk)
    serializer = MusicSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True): 
        serializer.save(artist=artist)
    return Response(serializer.data,status=status.HTTP_201_CREATED)
