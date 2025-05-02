from django.urls import path

from apps.events.apps import EventsConfig
from apps.events.views import (EventsCreateAPIView, EventsDeleteAPIView,
                               EventsDetailAPIView, EventsListAPIView,
                               EventsUpdateAPIView)

app_name = EventsConfig.name

urlpatterns = [
    path("", EventsCreateAPIView.as_view(), name="event_create"),
    path("<int:pk>", EventsUpdateAPIView.as_view(), name="event_update"),
    path("<int:pk>", EventsDeleteAPIView.as_view(), name="event_delete"),
    path("<int:pk>", EventsDetailAPIView.as_view(), name="event_detail"),
    path("", EventsListAPIView.as_view(), name="event_list"),
]
