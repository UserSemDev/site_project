from django.db import models


class Event(models.Model):
    """Модель мероприятия"""

    name = models.CharField(max_length=150, verbose_name="Название мероприятия")
    description = models.TextField(verbose_name="Описание мероприятия")
    event_date = models.DateTimeField(verbose_name="Дата проведения")
    available_tickets = models.IntegerField(verbose_name="Доступное количество билетов")
    ticket_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Стоимость билета"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
