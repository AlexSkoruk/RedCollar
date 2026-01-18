from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from .models import Message
from .serializers import MessageSerializer
from rest_framework import permissions 
class MessageViewSet(mixins.CreateModelMixin,  
                     viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer
    def create(self, request):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        try:
            lat = float(request.query_params['latitude'])
            lon = float(request.query_params['longitude'])
            radius = float(request.query_params.get('radius', 5))
        except (KeyError, ValueError):
            return Response({"error": "Required: latitude, longitude; optional: radius (km)"}, status=status.HTTP_400_BAD_REQUEST)

        center = Point(lon, lat, srid=4326)
        queryset = Message.objects.filter(point__location__distance_lte=(center, D(km=radius))).order_by('-created_at')
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)