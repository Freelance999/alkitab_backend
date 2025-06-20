from django.db import models

class Book(models.Model):
    abbr = models.CharField(max_length=255, default="")
    name = models.CharField(max_length=255, default="")
    chapter = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.abbr} - {self.name}"
    
class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    chapter = models.IntegerField(default=0)
    version = models.CharField(max_length=255, default="tb")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chapter {self.chapter} of {self.book.name}"
    
class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="verses")
    verse = models.IntegerField(default=0)
    type = models.CharField(max_length=255, default="")
    text = models.TextField(default="")
    version = models.CharField(max_length=255, default="tb")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Verse {self.verse} of Chapter {self.chapter.chapter} in {self.chapter.book.name}"