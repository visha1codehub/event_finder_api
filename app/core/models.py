"""
Models for Event Mangement System.
"""

from django.db import models


class Event(models.Model):
    """model for event."""
    event_name = models.CharField(max_length=254)
    city_name = models.CharField(max_length=254)
    date = models.DateField()
    time = models.TimeField()
    latitude = models.DecimalField(max_digits=20, decimal_places=15)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)

    def __str__(self):
        return self.event_name

    class Meta:
        ordering = ['date']
