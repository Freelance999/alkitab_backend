from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from alkitab_backend.models import SongBook
from alkitab_backend.serializers import SongBookSerializer

@api_view(['POST'])
def create_song_book(request):
    try:
        number = request.data.get('number')
        title = request.data.get('title')
        song_book_name = request.data.get('song_book_name', "KEE")
        author = request.data.get('author', "")
        song_url = request.FILES.get('song_url', None)

        if not number or not title or not song_book_name:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                "message": "All fields are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        SongBook.objects.create(number=number, title=title, song_book_name=song_book_name, author=author, song_url=song_url)

        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "Song book created successfully."
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def fetch_song_books(request, song_book_name="KEE"):
    try:
        song_books = SongBook.objects.filter(song_book_name=song_book_name).order_by('number')
        data = SongBookSerializer(song_books, many=True, context={'request': request}).data
        if not data:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "No song books found."
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": status.HTTP_200_OK,
            "message": "All song books fetched successfully.",
            'total_item': len(data),
            "data": data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)