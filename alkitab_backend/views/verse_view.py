import requests
import time
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from alkitab_backend.models import Book, Verse, Chapter
from alkitab_backend.serializers import BookSerializer, VerseSerializer

@api_view(['POST'])
def create_verse(request):
    try:
        abbr = request.data.get('abbr')
        name = request.data.get('name')
        chapter = request.data.get('chapter')

        if not abbr or not name:
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
def fetch_verse_by_abbr(request, abbr, chapter, version):
    try:
        book = Book.objects.filter(abbr=abbr).first()
        if not book:
            book = Book.objects.filter(name=abbr).first()
            if not book:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Book not found."
                }, status=status.HTTP_404_NOT_FOUND)

        chapter_obj = Chapter.objects.filter(book=book, chapter=chapter).first()
        if not chapter:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Chapter not found."
            }, status=status.HTTP_404_NOT_FOUND)

        verses = Verse.objects.filter(chapter=chapter_obj, version=version).order_by('verse')
        verse_content = Verse.objects.filter(chapter=chapter_obj, version=version, type="content").order_by('verse')
        data = VerseSerializer(verses, many=True).data
        for verse in data:
            verse['abbr'] = book.abbr
        total_verse = VerseSerializer(verse_content, many=True).data
        if not data:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "No verses found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        next_book = Book.objects.filter(id__gt=book.id).order_by('id').first()
        before_book = Book.objects.filter(id__lt=book.id).order_by('-id').first()
        if chapter < book.chapter:
            next_page = {
                "abbr": book.abbr,
                "name": book.name,
                "chapter": chapter + 1
            }
        else:
            next_book = Book.objects.filter(id__gt=book.id).order_by('id').first()
            if next_book:
                next_page = {
                    "abbr": next_book.abbr,
                    "name": next_book.name,
                    "chapter": 1
                }
            else:
                next_page = None

        if chapter > 1:
            before_page = {
                "abbr": book.abbr,
                "name": book.name,
                "chapter": chapter - 1
            }
        else:
            before_book = Book.objects.filter(id__lt=book.id).order_by('-id').first()
            if before_book:
                before_page = {
                    "abbr": before_book.abbr,
                    "name": before_book.name,
                    "chapter": before_book.chapter
                }
            else:
                before_page = None
        
        return Response({
            "status": status.HTTP_200_OK,
            "message": "All verses fetched successfully.",
            "total_item": len(data),
            "total_verse": len(total_verse),
            "data": {
                "book": BookSerializer(book).data,
                "chapter": chapter_obj.chapter,
                "verses": data
            },
            "before_page": before_page,
            "next_page": next_page
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def search_verse(request):
    try:
        query = request.GET.get('query')
        version = request.GET.get('version')
        page = int(request.GET.get('page'))
        page_size = int(request.GET.get('page_size'))

        if not query:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Query parameter 'query' is required."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        verses = Verse.objects.filter(text__icontains=query)
        if version:
            verses = verses.filter(version=version)
        verses = verses.order_by('chapter__book', 'chapter__chapter', 'verse')

        total_item = verses.count()
        start = (page - 1) * page_size
        end = start + page_size
        verses = verses[start:end]
        
        data = []
        for verse in verses:
            data.append({
                "id": verse.id,
                "book_name": verse.chapter.book.name,
                "book_abbr": verse.chapter.book.abbr,
                "chapter_number": verse.chapter.chapter,
                "chapter": verse.chapter.id,
                "verse": verse.verse,
                "type": verse.type,
                "text": verse.text,
                "version": verse.version,
                "created_at": verse.created_at,
                "updated_at": verse.updated_at,
            })

        return Response({
            "status": status.HTTP_200_OK,
            "message": "Verses search result.",
            "total_item": total_item,
            "page": page,
            "page_size": page_size,
            "total_page": (total_item + page_size - 1) // page_size,
            "data": data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def create_verses_from_api(request):
    abbr = request.data.get('abbr')
    chapter_num = request.data.get('chapter')
    version = request.data.get('version')

    if not abbr or not chapter_num:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "abbr and chapter are required."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        url = f"https://beeble.vercel.app/api/v1/passage/{abbr}/{chapter_num}?ver={version}"
        print("Ini url :", url)
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("data", {})

        book_name = data.get("book", {}).get("name")
        book_obj = Book.objects.filter(abbr=abbr).first()
        chapter = book_obj.chapter
        
        if  chapter < chapter_num: 
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": f"Chapter {chapter_num} exceeds the total chapters ({chapter}) in book '{book_name}'."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not book_obj:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": f"Book with abbr '{abbr}' not found."
            }, status=status.HTTP_404_NOT_FOUND)

        chapter_obj, _ = Chapter.objects.get_or_create(book=book_obj, chapter=chapter_num)

        verses_data = data.get("verses", [])
        created_verses = []
        for verse in verses_data:
            verse_num = verse.get("verse")
            verse_type = verse.get("type")
            text = verse.get("content")
            if not Verse.objects.filter(chapter=chapter_obj, verse=verse_num, version=version).exists():
                verse_obj = Verse.objects.create(
                    chapter=chapter_obj,
                    verse=verse_num,
                    type=verse_type,
                    text=text,
                    version=version
                )
                created_verses.append(VerseSerializer(verse_obj).data)

        return Response({
            "status": status.HTTP_201_CREATED,
            "message": f"{len(created_verses)} verses created.",
            "data": created_verses,
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def create_verses_bulk_from_api(request):
    abbr = request.data.get('abbr')
    start_chapter = int(request.data.get('chapter'))
    version = request.data.get('version')

    if not abbr or not version:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "abbr and version are required."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        book_obj = Book.objects.filter(abbr=abbr).first()
        if not book_obj:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": f"Book with abbr '{abbr}' not found."
            }, status=status.HTTP_404_NOT_FOUND)

        total_chapter = book_obj.chapter
        all_created_verses = []
        for chapter_num in range(start_chapter, total_chapter + 1):
            url = f"https://beeble.vercel.app/api/v1/passage/{abbr}/{chapter_num}?ver={version}"
            response = requests.get(url)
            if response.status_code != 200:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"Stopped at chapter {chapter_num}, API response: {response.status_code}"
                }, status=status.HTTP_400_BAD_REQUEST)
            data = response.json().get("data", {})

            chapter_obj, _ = Chapter.objects.get_or_create(book=book_obj, chapter=chapter_num)
            verses_data = data.get("verses", [])
            created_verses = []
            for verse in verses_data:
                verse_num = verse.get("verse")
                verse_type = verse.get("type")
                text = verse.get("content")
                if not Verse.objects.filter(chapter=chapter_obj, verse=verse_num, version=version).exists():
                    verse_obj = Verse.objects.create(
                        chapter=chapter_obj,
                        verse=verse_num,
                        type=verse_type,
                        text=text,
                        version=version
                    )
                    created_verses.append(VerseSerializer(verse_obj).data)
            all_created_verses.extend(created_verses)

            time.sleep(2)

        return Response({
            "status": status.HTTP_201_CREATED,
            "message": f"{len(all_created_verses)} verses created for {abbr} chapters {start_chapter}-{total_chapter}.",
            "data": all_created_verses,
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)