from support.constants import TicketStatus, SUPPORTED_COMPANY_DOMAINS
from support.errors import CompanyNotSupported
from support.models import Ticket as TicketModel, StaffUser
from support.providers.notifications import NotificationProvider


class TicketCreatorService:
    def __init__(self, notifications_provider: NotificationProvider):
        self.notifications_provider = notifications_provider

    @staticmethod
    def create_ticket(customer_email: str, issue: str) -> TicketModel:
        new_ticket = TicketModel.objects.create(customer_email=customer_email, issue=issue)
        return new_ticket

    @staticmethod
    def get_ticket(ticket_id: str) -> TicketModel:
        ticket = TicketModel.objects.get(pk=ticket_id)
        return ticket

    @staticmethod
    def assign(ticket: TicketModel):
        customer_company = ticket.customer_email.split('@')[1]  # example@example.com --> example.com
        if customer_company in SUPPORTED_COMPANY_DOMAINS:
            # If this is customer from Sibedge then assign ticket to the special company manager
            # otherwise to any random staff person
            if "sibedge.com" in customer_company:
                stuff_user = StaffUser.objects.get(name="SIBEDGE_Stuff")
            else:
                stuff_user = StaffUser.objects.exclude(name="SIBEDGE_Stuff").first()

            ticket.assigned_to = stuff_user
            ticket.save(update_fields=["assigned_to"])
        else:
            raise CompanyNotSupported(
                "Customers from this company are not supported. Ticket created but not assigned to anyone"
            )

    def mark_as_done(self, ticket_id: str):
        ticket = self.get_ticket(ticket_id)
        ticket.status = TicketStatus.DONE
        ticket.save(update_fields=["status"])

        self.notify_user_on_status_change(new_status=TicketStatus.DONE, customer_email=ticket.customer_email)

    def set_in_progress(self, ticket_id: str):
        ticket = self.get_ticket(ticket_id)
        ticket.status = TicketStatus.IN_PROGRESS
        ticket.save(update_fields=["status"])

        self.notify_user_on_status_change(new_status=TicketStatus.IN_PROGRESS, customer_email=ticket.customer_email)

    def process(self, ticket: TicketModel):
        self.assign(ticket=ticket)
        self.set_in_progress(ticket_id=ticket.pk)

    def notify_stuff_on_new_ticket_created(self, ticket_id: str, customer_email: str):
        """Send notification to stuff once new ticket created."""
        message = f'You have a new ticket created. ID: {ticket_id} from {customer_email}'
        self.notifications_provider.notify(to=customer_email, message=message)

    def notify_user_on_status_change(self, new_status: TicketStatus, customer_email: str):
        """Send email notification to customer that status of his ticket has changed."""
        message = f"The status of your ticket has changed and it's {new_status.label} now!"
        self.notifications_provider.notify(to=customer_email, message=message)
