from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from alkitab_backend.models import SongBook, TheLordsPrayer
from alkitab_backend.serializers import TheLordsPrayerSerializer

@api_view(['POST'])
def create_the_lords_prayer(request):
    try:
        text = request.data.get('text')
        version = request.data.get('version')

        if not text or not version:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                "message": "All fields are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        TheLordsPrayer.objects.create(text=text, version=version)

        return Response({
            "status": status.HTTP_201_CREATED,
            "message": "The Lord's Prayer created successfully."
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def fetch_the_lords_prayers(request, version):
    try:
        prayers = TheLordsPrayer.objects.filter(version=version)
        if not prayers.exists():
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "No The Lord's Prayer found for the specified version."
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": status.HTTP_200_OK,
            "message": "The Lord's Prayers fetched successfully.",
            "data": prayers.values('id', 'text', 'version', 'created_at', 'updated_at')
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)