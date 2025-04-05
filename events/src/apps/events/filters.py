import django_filters

from apps.events.models import Event


class EventFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="event_date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="event_date", lookup_expr="lte")

    class Meta:
        model = Event
        fields = ["date_from", "date_to"]
