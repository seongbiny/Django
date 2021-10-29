from rest_framework import serializers
from ..models import Album, Artist, Track


class AlbumListSerializer(serializers.ModelSerializer):
    # list
    class Meta:
        model = Album
        fields = ('pk', 'name',)


class AlbumSerializer(serializers.ModelSerializer):
   
    class ArtistSerializer(serializers.ModelSerializer):
        class Meta:
            model = Artist
            fields = ('pk', 'name', )

    class TrackSerializer(serializers.ModelSerializer):
        class Meta:
            model = Track
            fields = ('pk', 'title')

    name = serializers.CharField(min_length=2, max_length=100)
    tracks = TrackSerializer(many=True, read_only=True)
    artists = ArtistSerializer(many=True, read_only=True)
    
    artist_pks = serializers.ListField(write_only=True)

    def create(self, validated_data):
        artist_pks = validated_data.pop('artist_pks')
        album = Album.objects.create(**validated_data)

        for artist_pk in artist_pks:
            album.artists.add(artist_pk)
        
        return album

    def update(self, album, validated_data):
        artist_pks = validated_data.pop('artist_pks')

        for attr, value in validated_data.items():
            setattr(album, attr, value)
            album.save()
        
        # reset relation
        album.artists.clear()
        
        # set relation
        for artist_pk in artist_pks:
            album.artists.add(artist_pk)

        return album


    class Meta:
        model = Album
        fields = ('id', 'name', 'tracks', 'artists', 'artist_pks')