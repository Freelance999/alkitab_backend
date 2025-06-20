from django.contrib import admin
from .models import Book, Chapter, Verse

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'abbr', 'name', 'chapter', 'created_at', 'updated_at')

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'chapter', 'version', 'created_at', 'updated_at')

class VerseAdmin(admin.ModelAdmin):
    list_display = ('id', 'chapter', 'verse', 'type', 'text', 'version', 'created_at', 'updated_at')

admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Verse, VerseAdmin)