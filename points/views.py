from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point as GeosPoint
from django.contrib.gis.measure import D
from .models import Point
from .serializers import PointSerializer
from rest_framework import permissions  
from django.contrib.gis.db.models.functions import Distance

class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated]   
    
 

    def get_queryset(self):
        return self.queryset.order_by('-created_at') 

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        try:
            lat = float(request.query_params.get('latitude'))
            lon = float(request.query_params.get('longitude'))
            radius = float(request.query_params.get('radius', 10))  # по умолчанию 10 км
        except (TypeError, ValueError):
            return Response(
                {"error": "Необходимо передать latitude, longitude и radius (числа)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return Response(
                {"error": "Некорректные координаты"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if radius < 0:
            return Response(
                {"error": "Радиус не может быть отрицательным"},
                status=status.HTTP_400_BAD_REQUEST
            )

        center = GeosPoint(lon, lat, srid=4326)

        points = Point.objects.filter(
            location__distance_lte=(center, D(km=radius))
        ).annotate(
            distance=Distance('location', center)
        ).order_by('distance')

        serializer = self.get_serializer(points, many=True)
        return Response(serializer.data)