# Common app serializers
# This app contains utility serializers and common components

from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()


class APIInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    version = serializers.CharField()
    description = serializers.CharField()
