import datetime
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from alkitab_backend.models import Book, Verse, Chapter, Devotion, DevotionType
from alkitab_backend.serializers import BookSerializer, VerseSerializer, DevotionSerializer

@api_view(['POST'])
def create_devotion(request):
    try:
        title = request.data.get('title')
        book_id = request.data.get('book_id')
        devotion_id = request.data.get('devotion_id')
        chapter = request.data.get('chapter')
        start_verse = request.data.get('start_verse')
        end_verse = request.data.get('end_verse')
        date = request.data.get('date')
        text = request.data.get('text')

        if not title or not book_id or not chapter or not start_verse or not end_verse or not text:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                "message": "All fields are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        book = Book.objects.filter(id=book_id).first()
        chapter_obj = Chapter.objects.filter(book=book, chapter=chapter).first()
        chapter_id = chapter_obj.id
        verses = Verse.objects.filter(chapter=chapter_obj, verse__gte=start_verse, verse__lte=end_verse)
        if not book:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                "message": "Book not found."
            }, status=status.HTTP_404_NOT_FOUND)

        if not chapter_obj:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                "message": "Chapter not found."
            }, status=status.HTTP_404_NOT_FOUND)

        devotion_type = DevotionType.objects.filter(id=devotion_id).first()
        Devotion.objects.create(
            book=book, 
            chapter=chapter_obj, 
            devotion_type=devotion_type, 
            start_verse=start_verse, 
            end_verse=end_verse, 
            title=title, 
            date=date,
            text=text,
        )

        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "Daily meal created successfully.",
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def fetch_devotion(request, devotion_type_id):
    try:
        devotion_type = DevotionType.objects.filter(id=devotion_type_id).first()
        if not devotion_type:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Devotion Type not found."
            }, status=status.HTTP_404_NOT_FOUND)

        today = datetime.date.today()
        devotion = Devotion.objects.filter(devotion_type=devotion_type, date=today).first()
        if not devotion:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Devotion not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        book = Book.objects.filter(id=devotion.book.id).first()
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Devotion fetched successfully.",
            "data": {
                "devotion": DevotionSerializer(devotion).data,
                "book": BookSerializer(book).data,
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)