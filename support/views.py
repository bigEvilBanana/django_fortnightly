from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from support.forms import NewTicketForm
from support.models import Ticket, TicketStatus


class CreateTicketView(View):
    def get(self, request):
        context = {}
        return render(request, 'support/index.html', context)

    def post(self, request):
        context = {}
        form = NewTicketForm(request.POST)
        if form.is_valid():
            new_ticket = Ticket.objects.create(
                customer_email=form.cleaned_data['customer_email'],
                issue=form.cleaned_data['issue']
            )
            new_ticket.process()
            context.update({"done": True})
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
        ticket = Ticket.objects.filter(pk=int(ticket_pk)).first()
        ticket.mark_as_done()
        ticket.notify_user_on_status_change(new_status=TicketStatus.DONE)
        return HttpResponseRedirect(reverse('list-tickets'))


@method_decorator(csrf_exempt, name='dispatch')
class ReopenTicketView(View):

    def post(self, request):
        ticket_pk = request.POST['ticket']
        ticket = Ticket.objects.filter(pk=int(ticket_pk)).first()
        ticket.set_in_progress()
        ticket.notify_user_on_status_change(new_status=TicketStatus.IN_PROGRESS)
        return HttpResponseRedirect(reverse('list-tickets'))
