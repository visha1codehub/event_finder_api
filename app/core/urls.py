"""
Urls for event finder api.
"""
from django.urls import path
from . import views

urlpatterns = [
    # path("events/find/", views.event_list, name="event-list-api"),
    path("events/find/", views.EventList.as_view(), name="event-list-api"),
]
