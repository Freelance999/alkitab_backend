from rest_framework import serializers
from . import models

class BookSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Book
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Chapter
        fields = '__all__'
        
class VerseSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Verse
        fields = '__all__'

class DevotionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Devotion
        fields = '__all__'

class DevotionTypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.DevotionType
        fields = '__all__'

class ReadingPlanSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.ReadingPlan
        fields = '__all__'

class ReadingPlanBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta(object):
        model = models.ReadingPlanBook
        fields = '__all__'

class SongBookSerializer(serializers.ModelSerializer):
    song_url = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta(object):
        model = models.SongBook
        fields = '__all__'

    def get_song_url(self, obj):
        request = self.context.get('request')
        if obj.song_url and hasattr(obj.song_url, 'url'):
            return request.build_absolute_uri(obj.song_url.url) if request else obj.song_url.url
        return None

    def get_duration(self, obj):
        return obj.get_duration()

class SongSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Song
        fields = '__all__'

class TheLordsPrayerSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.TheLordsPrayer
        fields = '__all__'