from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Announcement
from .serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['target_audience', 'priority', 'is_published']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'priority']

    def get_queryset(self):
        user = self.request.user
        queryset = Announcement.objects.filter(is_published=True)
        
        # Filter by target audience
        if user.role == 'student':
            queryset = queryset.filter(target_audience__in=['all', 'students'])
        elif user.role == 'professor':
            queryset = queryset.filter(target_audience__in=['all', 'professors'])
        elif user.role == 'staff':
            queryset = queryset.filter(target_audience__in=['all', 'staff'])
        elif user.role == 'admin':
            queryset = Announcement.objects.all()  # Admins see everything
            
        return queryset
