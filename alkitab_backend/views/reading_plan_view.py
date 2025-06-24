from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from alkitab_backend.models import ReadingPlan
from alkitab_backend.serializers import ReadingPlanSerializer

@api_view(['POST'])
def create_reading_plan(request):
    try:
        title = request.data.get('title')
        description = request.data.get('description')
        length = request.data.get('length')
        download = request.data.get('download', 0)
        finished = request.data.get('finished', 0.0)
        is_on_schedule = request.data.get('is_on_schedule', False)

        if not title or not description or not length:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                "message": "All fields are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        ReadingPlan.objects.create(title=title, description=description, length=length, download=download, finished=finished, is_on_schedule=is_on_schedule)

        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "Reading plan created successfully."
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def fetch_reading_plans(request):
    try:
        reading_plans = ReadingPlan.objects.all().order_by('-updated_at')
        data = ReadingPlanSerializer(reading_plans, many=True).data
        if not data:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "No reading plans found."
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": status.HTTP_200_OK,
            "message": "All reading plans fetched successfully.",
            'total_item': len(data),
            "data": data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
def update_download(request, id):
    try:
        reading_plans = ReadingPlan.objects.filter(id=id).first()
        if not reading_plans:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Reading plan not found."
            }, status=status.HTTP_404_NOT_FOUND)

        reading_plans.download += 1
        reading_plans.save()

        return Response({
            "status": status.HTTP_200_OK,
            "message": "Download incremented successfully.",
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)