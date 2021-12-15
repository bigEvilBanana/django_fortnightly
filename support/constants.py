from django.db import models


class TicketStatus(models.IntegerChoices):
    NEW = 10
    IN_PROGRESS = 20
    DONE = 30


SUPPORTED_COMPANY_DOMAINS = (
    "example.com",
    "yandex.ru",
    "sibedge.com"
)