from django.utils import timezone
from rest_framework import serializers

from apps.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Сериализатор мероприятий"""

    class Meta:
        model = Event
        fields = "__all__"

    def validate_event_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Дата мероприятия не может быть в прошлом"
            )
        return value

    def validate(self, data):
        available_tickets = data.get("available_tickets")
        ticket_price = data.get("ticket_price")

        if available_tickets is not None and available_tickets <= 0:
            raise serializers.ValidationError(
                "Доступное количество билетов должно быть больше нуля"
            )

        if ticket_price is not None and ticket_price <= 0:
            raise serializers.ValidationError(
                "Стоимость билета должна быть больше нуля"
            )

        return data
