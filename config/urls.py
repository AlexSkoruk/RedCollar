from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from points.views import PointViewSet
from point_messages.views import MessageViewSet

points_router = DefaultRouter()
points_router.register(r'points', PointViewSet, basename='point')

messages_router = DefaultRouter()
messages_router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(points_router.urls)),
    path('api/', include(messages_router.urls)),
]