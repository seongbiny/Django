from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Artist, Album, Track

from .serializers.artist import ArtistListSerializer, ArtistSerializer
from .serializers.album import AlbumListSerializer, AlbumSerializer
from .serializers.track import TopTrackListSerializer, TrackSerializer


@api_view(['GET', 'POST'])
def artist_list_or_create(request):
    
    def artist_list():
        artists = Artist.objects.all()
        serializer = ArtistListSerializer(artists, many=True)
        return Response(serializer.data)

    def create_artist():
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    if request.method == 'GET':
        return artist_list()
    elif request.method == 'POST':
        return create_artist()


@api_view(['GET', 'PUT', 'DELETE'])
def artist_detail_or_update_or_delete(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)

    def artist_detail():
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def update_artist():
        serializer = ArtistSerializer(instance=artist, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete_artist():
        artist.delete()
        return Response(data='delete successfully', status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        return artist_detail()
    elif request.method == 'PUT':
        return update_artist()
    elif request.method == 'DELETE':
        return delete_artist()


@api_view(['GET', 'POST'])
def album_list_or_create(request):

    if request.method == 'GET':
        albums = Album.objects.all()
        serializer = AlbumListSerializer(albums, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def album_detail_or_update_or_delete(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    
    if request.method == 'GET':
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AlbumSerializer(instance=album, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        album.delete()
        return Response(data='delete successfully', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def top_track_list(request):
    # tracks = Track.objects.order_by('-click')
    tracks = Track.objects\
            .prefetch_related('artists')\
            .select_related('album')\
            .order_by('-click')\

    serializer = TopTrackListSerializer(tracks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_track(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    serializer = TrackSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(album=album)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def track_detail_or_update_or_delete(request, album_pk, track_pk):
    album = get_object_or_404(Album, pk=album_pk)
    
    # track = get_object_or_404(Track, pk=track_pk)
    
    qs = Track.objects\
            .prefetch_related('artists')\
            .select_related('album')
    
    track = get_object_or_404(qs, pk=track_pk)

    def track_detail():
        track.click += 1
        track.save()
        serializer = TrackSerializer(track)
        return Response(serializer.data)

    def update_track():
        serializer = TrackSerializer(instance=track, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(album=album)
            return Response(serializer.data)
    
    def delete_track():
        track.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        return track_detail()
    elif request.method == 'PUT':
        return update_track()
    else:
        return delete_track()