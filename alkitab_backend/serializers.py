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