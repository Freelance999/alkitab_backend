from django.contrib import admin
from .models import Book, Chapter, Verse, Devotion, DevotionType

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

admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Verse, VerseAdmin)
admin.site.register(Devotion, DevotionAdmin)
admin.site.register(DevotionType, DevotionTypeAdmin)