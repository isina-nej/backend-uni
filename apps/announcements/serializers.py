from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'author', 'author_name', 'target_audience', 
                 'priority', 'is_published', 'created_at', 'updated_at', 'expires_at']
