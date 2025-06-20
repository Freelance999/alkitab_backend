import requests
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from alkitab_backend.models import Book
from alkitab_backend.serializers import BookSerializer
# Ini test commit and push
@api_view(['POST'])
def create_book(request):
    try:
        abbr = request.data.get('abbr')
        name = request.data.get('name')
        chapter = request.data.get('chapter')

        if not abbr and not name:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                "message": "Abbreviation and name are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        Book.objects.create(abbr=abbr, name=name, chapter=chapter)

        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "Book created successfully.",
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def fetch_books(request):
    try:
        books = Book.objects.all()
        data = BookSerializer(books, many=True).data
        if not data:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "No books found."
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": status.HTTP_200_OK,
            "message": "All books fetched successfully.",
            'total_item': len(data),
            "data": data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def create_books_from_api(request):
    try:
        url = "https://beeble.vercel.app/api/v1/passage/list"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("data", [])

        created_books = []
        for item in data:
            abbr = item.get("abbr")
            name = item.get("name")
            chapter = item.get("chapter")

            if not Book.objects.filter(abbr=abbr, name=name).exists():
                book = Book.objects.create(abbr=abbr, name=name, chapter=chapter)
                created_books.append(BookSerializer(book).data)

        return Response({
            "status": status.HTTP_201_CREATED,
            "message": f"{len(created_books)} books created.",
            "data": created_books,
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)