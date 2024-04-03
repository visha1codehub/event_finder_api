"""
Urls for event finder api.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("sync/", views.SyncEventListView.as_view(), name="event-list"),
    path("create-event/", views.EventCreateView.as_view(), name="event-create"),
    path("async/", views.AsyncEventListView.as_view(), name="async-event-list"),
]
