# Generated by Django 5.1.7 on 2025-04-04 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=150, verbose_name="Название мероприятия"
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание мероприятия")),
                ("event_date", models.DateTimeField(verbose_name="Дата проведения")),
                (
                    "available_tickets",
                    models.IntegerField(verbose_name="Доступное количество билетов"),
                ),
                (
                    "ticket_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=9, verbose_name="Стоимость билета"
                    ),
                ),
            ],
            options={
                "verbose_name": "Мероприятие",
                "verbose_name_plural": "Мероприятия",
            },
        ),
    ]
