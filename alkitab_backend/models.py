import os
from django.db import models
from mutagen.mp3 import MP3
from django.conf import settings

class Book(models.Model):
    abbr = models.CharField(max_length=255, default="")
    name = models.CharField(max_length=255, default="")
    chapter = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    chapter = models.IntegerField(default=0)
    version = models.CharField(max_length=255, default="tb")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.name} BAB {self.chapter}"
    
class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="verses")
    verse = models.IntegerField(default=0)
    type = models.CharField(max_length=255, default="")
    text = models.TextField(default="")
    version = models.CharField(max_length=255, default="tb")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"BAB {self.chapter.chapter} Ayat {self.verse}"
    
class DevotionType(models.Model):
    name = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Devotion(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="devotions")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="devotions")
    devotion_type = models.ForeignKey(DevotionType, on_delete=models.CASCADE, related_name="devotions", default=None, null=True)
    start_verse = models.IntegerField(default=0)
    end_verse = models.IntegerField(default=0)
    title = models.CharField(max_length=255, default="")
    text = models.TextField(default="")
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.book.name} BAB {self.chapter.chapter}"
    
class ReadingPlan(models.Model):
    title = models.CharField(max_length=255, default="")
    description = models.TextField(default="")
    length = models.IntegerField(default=0)
    download = models.IntegerField(default=0)
    finished = models.FloatField(default=0.0)
    is_on_schedule = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.length} hari"
    
class ReadingPlanBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reading_plan_books")
    reading_plan = models.ForeignKey(ReadingPlan, on_delete=models.CASCADE, related_name="reading_plan_books")
    start_chapter = models.IntegerField(default=0)
    end_chapter = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reading_plan.title} - {self.book.name}"
    
class SongBook(models.Model):
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=255, default="")
    song_book_name = models.CharField(max_length=255, default="")
    author = models.CharField(max_length=255, default="", null=True, blank=True)
    song_url = models.FileField(upload_to='songs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_duration(self):
        if self.song_url and self.song_url.path:
            file_path = os.path.join(settings.MEDIA_ROOT, self.song_url.name)
            try:
                audio = MP3(file_path)
                return round(audio.info.length, 2) 
            except Exception as e:
                return None
        return None

    def __str__(self):
        return f"{self.number}. {self.title}"
    
class Song(models.Model):
    song_book = models.ForeignKey(SongBook, on_delete=models.CASCADE, related_name="songs")
    number = models.IntegerField(default=0)
    text = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.number)
    
class TheLordsPrayer(models.Model):
    text = models.TextField(default="")
    version = models.CharField(max_length=255, default="tb")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Versi {self.version}"