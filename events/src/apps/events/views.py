from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from apps.events.filters import EventFilter
from apps.events.models import Event
from apps.events.pagination import EventPagination
from apps.events.serializers import EventSerializer
from apps.events.permissions import IsAdmin


class EventsCreateAPIView(generics.CreateAPIView):
    """Эндпоинт создания мероприятия"""
    permission_classes = [IsAdmin]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventsUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт изменения мероприятия"""
    permission_classes = [IsAdmin]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventsDeleteAPIView(generics.DestroyAPIView):
    """Эндпоинт удаления мероприятия"""
    permission_classes = [IsAdmin]
    queryset = Event.objects.all()


class EventsDetailAPIView(generics.RetrieveAPIView):
    """Эндпоинт детального просмотра мероприятия"""

    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventsListAPIView(generics.ListAPIView):
    """Эндпоинт списка мероприятий"""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EventFilter
    ordering_fields = ["event_date"]
    ordering = ["event_date"]

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data["total_count"] = self.paginator.page.paginator.count
        response.data["page_size"] = len(data)
        return response
