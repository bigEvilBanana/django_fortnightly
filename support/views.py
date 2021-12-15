from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from support.errors import CompanyNotSupported
from support.forms import NewTicketForm
from support.models import Ticket
from support.providers.notifications import EmailNotificationProvider
from support.services.ticket_creator import TicketCreatorService

NOTIFICATION_PROVIDER = EmailNotificationProvider()
ticket_service = TicketCreatorService(notifications_provider=NOTIFICATION_PROVIDER)


class CreateTicketView(View):

    def get(self, request):
        context = {}
        return render(request, 'support/index.html', context)

    def post(self, request):
        context = {}
        form = NewTicketForm(request.POST)

        if form.is_valid():
            new_ticket = ticket_service.create_ticket(
                customer_email=form.cleaned_data['customer_email'], issue=form.cleaned_data['issue']
            )

            try:
                ticket_service.process(ticket=new_ticket)
                context.update({"done": True})
            except CompanyNotSupported as e:
                context.update({"done": False, "error": e.message})

        return render(request, 'support/index.html', context)


class ListTickets(View):
    def get(self, request):
        tickets = Ticket.objects.order_by('status').all()
        context = {
            "tickets": tickets,
        }
        return render(request, 'support/ticket_list.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class ResolveTicketView(View):

    def post(self, request):
        ticket_pk = request.POST['ticket']
        ticket_service.mark_as_done(ticket_id=ticket_pk)
        return HttpResponseRedirect(reverse('list-tickets'))


@method_decorator(csrf_exempt, name='dispatch')
class ReopenTicketView(View):

    def post(self, request):
        ticket_pk = request.POST['ticket']
        ticket_service.set_in_progress(ticket_id=ticket_pk)
        return HttpResponseRedirect(reverse('list-tickets'))
