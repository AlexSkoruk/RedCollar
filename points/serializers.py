from rest_framework import serializers
from django.contrib.gis.geos import Point, fromstr
from .models import Point

class PointSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField(write_only=True)
    latitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Point
        fields = ['id', 'title', 'longitude', 'latitude', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        lon = validated_data.pop('longitude')
        lat = validated_data.pop('latitude')
        
        location = fromstr(f'POINT({lon} {lat})', srid=4326)    
        
        validated_data['location'] = location
        return super().create(validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['longitude'] = instance.location.x
        ret['latitude'] = instance.location.y
        return ret