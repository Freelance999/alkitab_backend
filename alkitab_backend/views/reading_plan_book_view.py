from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from alkitab_backend.models import ReadingPlan, ReadingPlanBook
from alkitab_backend.serializers import ReadingPlanSerializer, ReadingPlanBookSerializer

@api_view(['POST'])
def create_reading_plan_book(request):
    try:
        book_id = request.data.get('book_id')
        reading_plan_id = request.data.get('reading_plan_id')
        start_chapter = request.data.get('start_chapter')
        end_chapter = request.data.get('end_chapter')
        is_finished = request.data.get('is_finished', False)

        if not book_id or not reading_plan_id or not start_chapter or not end_chapter:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                "message": "All fields are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        ReadingPlanBook.objects.create(book_id=book_id, reading_plan_id=reading_plan_id, start_chapter=start_chapter, end_chapter=end_chapter, is_finished=is_finished)

        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "Reading plan book created successfully."
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def fetch_reading_plan_books(request, reading_plan_id):
    try:
        reading_plan = ReadingPlan.objects.filter(id=reading_plan_id).first()
        if not reading_plan:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Reading plan not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
        reading_plan_books = ReadingPlanBook.objects.filter(reading_plan=reading_plan)
        data = ReadingPlanBookSerializer(reading_plan_books, many=True).data
        if not data:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "No reading plan books found."
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": status.HTTP_200_OK,
            "message": "All reading plan books fetched successfully.",
            'total_item': len(data),
            "data": {
                "reading_plan": ReadingPlanSerializer(reading_plan).data,
                "reading_plan_books": data
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)