"""
Urls for event finder api.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("sync/", views.SyncEventListView.as_view(), name="event-list"),
    path("create/", views.EventCreateView.as_view(), name="event-create"),
    path("async/", views.AsyncEventListView.as_view(), name="async-event-list"),
    path("thread/", views.ThreadEventListView.as_view(), name="thread-event-list"),
]
