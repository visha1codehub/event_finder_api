"""
Urls for event finder api.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.EventListView.as_view(), name="event-list"),
    path("create-event/", views.EventCreateView.as_view(), name="event-create"),
    # path("events/find/", views.EventList.as_view(), name="async-event-list"),
]
