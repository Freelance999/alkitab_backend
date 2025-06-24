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

class ReadingPlanSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.ReadingPlan
        fields = '__all__'

class ReadingPlanBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta(object):
        model = models.ReadingPlanBook
        fields = '__all__'