from django.db import models

from support.constants import TicketStatus


class StaffUser(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)

    def __str__(self):
        return f'{self.name} :: {self.email}'


class Ticket(models.Model):
    issue = models.TextField(null=False, blank=False)
    status = models.IntegerField(choices=TicketStatus.choices, default=TicketStatus.NEW, null=False, blank=False)
    customer_email = models.EmailField(null=False, blank=False)
    assigned_to = models.ForeignKey(StaffUser, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f'{self.customer_email}: {self.issue[:30]}...'
