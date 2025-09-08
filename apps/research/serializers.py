from rest_framework import serializers
from .models import ResearchProject


class ResearchProjectSerializer(serializers.ModelSerializer):
    lead_researcher_name = serializers.CharField(source='lead_researcher.username', read_only=True)
    team_members_names = serializers.SerializerMethodField()

    class Meta:
        model = ResearchProject
        fields = ['id', 'title', 'description', 'lead_researcher', 'lead_researcher_name', 'team_members', 'team_members_names', 'start_date', 'end_date', 'status']

    def get_team_members_names(self, obj):
        return [member.username for member in obj.team_members.all()]
