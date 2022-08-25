from rest_framework import serializers
from api.models import Result


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('title', 'description', 'thumbnail', 'video_id', 'publish_time')
        read_only_fields = ('title', 'description', 'thumbnail', 'video_id', 'publish_time')
