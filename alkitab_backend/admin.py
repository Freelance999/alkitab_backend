from django.contrib import admin
from .models import Book, Chapter, Verse, Devotion, DevotionType, ReadingPlan, ReadingPlanBook, SongBook, Song, TheLordsPrayer

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'abbr', 'name', 'chapter', 'created_at', 'updated_at')

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'chapter', 'version', 'created_at', 'updated_at')

class VerseAdmin(admin.ModelAdmin):
    list_display = ('id', 'chapter', 'verse', 'type', 'text', 'version', 'created_at', 'updated_at')

class DevotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'chapter', 'devotion_type', 'start_verse', 'end_verse', 'title', 'text', 'date', 'created_at', 'updated_at')

class DevotionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')

class ReadingPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'length', 'download', 'finished', 'is_on_schedule', 'created_at', 'updated_at')

class ReadingPlanBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'reading_plan', 'start_chapter', 'end_chapter', 'is_finished', 'created_at', 'updated_at')

class SongBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'title', 'song_book_name', 'author', 'song_url', 'created_at', 'updated_at')

class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'song_book', 'number', 'text', 'created_at', 'updated_at')

class TheLordsPrayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'version', 'created_at', 'updated_at')

admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Verse, VerseAdmin)
admin.site.register(Devotion, DevotionAdmin)
admin.site.register(DevotionType, DevotionTypeAdmin)
admin.site.register(ReadingPlan, ReadingPlanAdmin)
admin.site.register(ReadingPlanBook, ReadingPlanBookAdmin)
admin.site.register(SongBook, SongBookAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(TheLordsPrayer, TheLordsPrayerAdmin)