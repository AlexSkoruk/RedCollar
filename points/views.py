from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from .models import Point
from .serializers import PointSerializer
from rest_framework import permissions  

class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated]   
    
 

    def get_queryset(self):
        return self.queryset.order_by('-created_at') 

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request, *args, **kwargs):

        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        radius = request.query_params.get('radius')

        if latitude and longitude:
            try:
                lat = float(latitude)
                lon = float(longitude)
                rad = float(radius) if radius else 5.0
            except ValueError:
                return Response(
                    {"error": "latitude, longitude должны быть числами"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            center = Point(lon, lat, srid=4326)
            queryset = Point.objects.filter(
                location__distance_lte=(center, D(km=rad))
            ).order_by('created_at')
        else:
            queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)