from django.contrib import admin

from support.models import Ticket, StaffUser


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('customer_email', 'status', 'assigned_to')


admin.site.register(StaffUser)
