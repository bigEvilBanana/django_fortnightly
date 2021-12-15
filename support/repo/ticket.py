from typing import Optional

from support.models import Ticket


def create_ticket(customer_email: str, issue: str) -> Optional[Ticket]:
    new_ticket = Ticket.objects.create(customer_email=customer_email, issue=issue)
    return new_ticket


def get_ticket_by_id(ticket_id: int) -> Optional[Ticket]:
    new_ticket = Ticket.objects.get(pk=ticket_id)
    return new_ticket
