from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from alkitab_backend.models import Song, SongBook
from alkitab_backend.serializers import SongBookSerializer, SongSerializer

@api_view(['POST'])
def create_song(request):
    try:
        song_book_id = request.data.get('song_book_id')
        number = request.data.get('number')
        text = request.data.get('text')

        if song_book_id is None or number is None or text is None:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                "message": "All fields are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        Song.objects.create(song_book_id=song_book_id, number=number, text=text)

        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "Song created successfully."
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def fetch_songs(request, song_book_id):
    try:
        song_book = SongBook.objects.filter(id=song_book_id).first()
        songs = Song.objects.filter(song_book=song_book).order_by('number')
        data = SongSerializer(songs, many=True, context={'request': request}).data

        if not song_book:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Song book not found."
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": status.HTTP_200_OK,
            "message": "All songs fetched successfully.",
            'total_item': len(data),
            "data": {
                "song_book": SongBookSerializer(song_book, context={'request': request}).data,
                "songs": data
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)