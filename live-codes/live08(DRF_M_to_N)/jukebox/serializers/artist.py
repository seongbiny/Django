from rest_framework import serializers
from ..models import Artist, Track, Album


# 1. validation (C, U)      - Write
# 2. 데이터의 구조를 결정 (R)  - Read
class ArtistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name',)


class ArtistSerializer(serializers.ModelSerializer):
    
    class TrackSerializer(serializers.ModelSerializer):
        class Meta:
            model = Track
            fields = ('id', 'title')
    
    class AlbumSerializer(serializers.ModelSerializer):
        class Meta:
            model = Album
            fields = ('id', 'name')

    name = serializers.CharField(min_length=1, max_length=100)
    tracks = TrackSerializer(many=True, read_only=True)
    albums = AlbumSerializer(many=True, read_only=True)
    album_count = serializers.IntegerField(
        source='albums.count',
        read_only=True
    )

    class Meta:
        model = Artist
        fields = ('id', 'name', 'debut', 'albums', 'tracks', 'album_count')
