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
        return f"Verse {self.verse} of Chapter {self.chapter.chapter}"
    
class DevotionType(models.Model):
    name = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Devotion Type: {self.name}"
    
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
        return f"Devotion '{self.title}' for {self.book.name} - Chapter {self.chapter.chapter}"
    
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
        return f"Reading Plan: {self.title} ({self.length} days)"
    
class ReadingPlanBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reading_plan_books")
    reading_plan = models.ForeignKey(ReadingPlan, on_delete=models.CASCADE, related_name="reading_plan_books")
    start_chapter = models.IntegerField(default=0)
    end_chapter = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reading Plan Book: {self.book.name} in {self.reading_plan.title}"
    
class SongBook(models.Model):
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=255, default="")
    song_book_name = models.CharField(max_length=255, default="")
    author = models.CharField(max_length=255, default="", null=True, blank=True)
    song_url = models.FileField(upload_to='songs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Song Book: {self.title} ({self.number})"
    
class Song(models.Model):
    song_book = models.ForeignKey(SongBook, on_delete=models.CASCADE, related_name="songs")
    number = models.IntegerField(default=0)
    text = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Song: {self.number}"
    
class TheLordsPrayer(models.Model):
    text = models.TextField(default="")
    version = models.CharField(max_length=255, default="tb")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"The Lord's Prayer ({self.version})"