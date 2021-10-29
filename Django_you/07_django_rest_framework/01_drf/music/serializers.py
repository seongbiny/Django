from rest_framework import serializers

from .models import Music, Artist

class MusicListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ('id', 'name')

class MusicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Music
        fields = '__all__'

class ArtistListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ('id', 'name',)

class ArtistSerializer(serializers.ModelSerializer):
    music_set = MusicSerializer(many=True)
    music_count = serializers.IntegerField(source='music_set.count')

    class Meta:
        model = Artist
        fields = '__all__'