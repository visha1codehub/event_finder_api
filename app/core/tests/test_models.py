"""
Tests for models.
"""

from decimal import Decimal
from datetime import date, time

from django.test import TestCase
from django.core.exceptions import ValidationError

from core.models import Event


class EventModelTests(TestCase):
    "Test Event model."

    def test_create_event(self):
        """Test creating a event is successful."""
        event = Event.objects.create(
            event_name="Test Event",
            city_name="Test City",
            date=date(2024, 4, 4),
            time=time(15, 30),
            latitude=Decimal('-75.8756654643'),
            longitude=Decimal('2.23323643'),
        )
        events = Event.objects.all()

        self.assertEqual(len(events), 1)
        self.assertIsNotNone(event.id)
        self.assertEqual(str(event), event.event_name)

    def test_event_ordering(self):
        """Test event is ordered by its date."""

        after = Event.objects.create(
            event_name="Test Event after",
            city_name="Test City2",
            date=date(2024, 4, 15),
            time=time(15, 30),
            latitude=Decimal('-75.8756654643'),
            longitude=Decimal('2.23323643'),
        )
        before = Event.objects.create(
            event_name="Test Event before",
            city_name="Test City2",
            date=date(2024, 4, 6),
            time=time(10, 00),
            latitude=Decimal('-75.8756654643'),
            longitude=Decimal('2.23323643'),
        )

        self.assertEqual(str(after), after.event_name)
        self.assertEqual(str(before), before.event_name)
        events = Event.objects.all()
        self.assertEqual(events[0], before)

    def test_event_name_max_length(self):
        """Test that the event_name field enforces the maximum length."""

        long_name = "a" * 255
        event = Event(
            event_name=long_name,
            city_name="Test City",
            date=date(2024, 4, 4),
            time=time(15, 30),
            latitude=Decimal('-75.8756654643'),
            longitude=Decimal('2.23323643'),
            )

        # with self.assertRaises(ValidationError):
        #     event.full_clean()                      # or
        self.assertRaises(ValidationError, event.full_clean)
