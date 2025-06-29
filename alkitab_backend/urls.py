from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from alkitab_backend.views.book_view import create_book, create_books_from_api, fetch_books
from alkitab_backend.views.verse_view import create_verses_from_api, fetch_verse_by_abbr, create_verses_bulk_from_api, search_verse
from alkitab_backend.views.devotion_view import create_devotion, fetch_devotion
from alkitab_backend.views.reading_plan_view import create_reading_plan, fetch_reading_plans, update_download
from alkitab_backend.views.reading_plan_book_view import create_reading_plan_book, fetch_reading_plan_books
from alkitab_backend.views.song_book_view import create_song_book, fetch_song_books
from alkitab_backend.views.song_view import create_song, fetch_songs
from alkitab_backend.views.the_lords_prayer_view import fetch_the_lords_prayers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gbkp/v1/book/create-from-api', create_books_from_api),
    path('api/gbkp/v1/book/create', create_book),
    path('api/gbkp/v1/book/fetch', fetch_books),
    path('api/gbkp/v1/verse/create-from-api', create_verses_from_api),
    path('api/gbkp/v1/verse/fetch/<str:abbr>/<int:chapter>/<str:version>', fetch_verse_by_abbr),
    path('api/gbkp/v1/verse/bulk-create-from-api', create_verses_bulk_from_api),
    path('api/gbkp/v1/verse/search', search_verse),
    path('api/gbkp/v1/devotion/create', create_devotion),
    path('api/gbkp/v1/devotion/fetch/<int:devotion_type_id>', fetch_devotion),
    path('api/gbkp/v1/reading-plan/create', create_reading_plan),
    path('api/gbkp/v1/reading-plan/fetch', fetch_reading_plans),
    path('api/gbkp/v1/reading-plan/update/<int:id>', update_download),
    path('api/gbkp/v1/reading-plan-book/create', create_reading_plan_book),
    path('api/gbkp/v1/reading-plan-book/fetch/<int:reading_plan_id>', fetch_reading_plan_books),
    path('api/gbkp/v1/song-book/create', create_song_book),
    path('api/gbkp/v1/song-book/fetch/<str:song_book_name>', fetch_song_books),
    path('api/gbkp/v1/song/create', create_song),
    path('api/gbkp/v1/song/fetch/<int:song_book_id>', fetch_songs),
    path('api/gbkp/v1/song/fetch/<int:song_book_id>', fetch_songs),
    path('api/gbkp/v1/the-lords-prayer/fetch/<str:version>', fetch_the_lords_prayers),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)