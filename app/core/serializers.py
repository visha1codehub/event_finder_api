"""
Serializers for event finder APIs..
"""
from rest_framework import serializers

from .models import Event


class EventListSerializer(serializers.ModelSerializer):
    """Serializer for event list."""
    class Meta:
        model = Event
        fields = ['event_name', 'city_name', 'date', 'time', 'latitude', 'longitude',]
