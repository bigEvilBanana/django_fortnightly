from django.db import models

from support.constants import TicketStatus, SUPPORTED_COMPANY_DOMAINS
from support.errors import CompanyNotSupported
from support.utils import send_email_notification


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

    def assign(self):
        customer_company = self.customer_email.split('@')[1]  # example@example.com --> example.com
        if customer_company in SUPPORTED_COMPANY_DOMAINS:
            # If this is customer from Sibedge then assign ticket to the special company manager
            # otherwise to any random staff person
            if "sibedge.com" in customer_company:
                self.assigned_to = StaffUser.objects.get(name="SIBEDGE_Stuff")
            else:
                self.assigned_to = StaffUser.objects.exclude(name="SIBEDGE_Stuff").first()
            self.save(update_fields=["assigned_to"])
        else:
            raise CompanyNotSupported(
                "Customers from this company are not supported. Ticket created but not assigned to anyone"
            )

    def process(self):
        self.assign()
        self.set_in_progress()
        self.notify_user_on_status_change(new_status=self.status)

    def mark_as_done(self):
        self.status = TicketStatus.DONE
        self.save(update_fields=["status"])

    def set_in_progress(self):
        self.status = TicketStatus.IN_PROGRESS
        self.save(update_fields=["status"])

    def notify_stuff_on_new_ticket_created(self):
        """Send email notification to stuff once new ticket created."""
        # TODO: этот метод относится к Ticket или StaffUser?
        message = f'You have a new ticket created. ID: {self.pk} from {self.customer_email}'
        send_email_notification(to=self.assigned_to.email, message=message)

    def notify_user_on_status_change(self, new_status: TicketStatus):
        """Send email notification to customer that status of his ticket has changed."""
        message = f"The status of your ticket has changed and it's {new_status.label} now!"
        send_email_notification(to=self.customer_email, message=message)
