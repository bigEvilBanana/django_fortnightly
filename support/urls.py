from django.urls import path

from support import views

urlpatterns = [
    path('', views.CreateTicketView.as_view(), name='index'),
    path('tickets/', views.ListTickets.as_view(), name='list-tickets'),
    path('tickets/resolve/', views.ResolveTicketView.as_view(), name='resolve-ticket'),
    path('tickets/reopen/', views.ReopenTicketView.as_view(), name='reopen-ticket'),
]