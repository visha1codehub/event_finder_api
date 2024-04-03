"""
Urls for event finder api.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("api/events/", views.EventAPIView.as_view(), name="event-list"),
    # path("events/find/", views.EventList.as_view(), name="async-event-list"),
]
