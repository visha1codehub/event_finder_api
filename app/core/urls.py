"""
Urls for event finder api.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("sync/", views.EventListView.as_view(), name="event-list"),
    path("create-event/", views.EventCreateView.as_view(), name="event-create"),
    path("async/", views.AsyncEventList.as_view(), name="async-event-list"),
]
