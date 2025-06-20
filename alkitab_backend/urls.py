from django.contrib import admin
from django.urls import path
from alkitab_backend.views.book_view import create_book, create_books_from_api, fetch_books
from alkitab_backend.views.verse_view import create_verses_from_api, fetch_verse_by_abbr, create_verses_bulk_from_api, search_verse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gbkp/v1/book/create-from-api', create_books_from_api),
    path('api/gbkp/v1/book/create', create_book),
    path('api/gbkp/v1/book/fetch', fetch_books),
    path('api/gbkp/v1/verse/create-from-api', create_verses_from_api),
    path('api/gbkp/v1/verse/fetch/<str:abbr>/<int:chapter>/<str:version>', fetch_verse_by_abbr),
    path('api/gbkp/v1/verse/bulk-create-from-api', create_verses_bulk_from_api),
    path('api/gbkp/v1/verse/search', search_verse),
]
