from django.urls import path

from src.apps.ws_authentication import views

urlpatterns = [
    path("tickets/", views.TicketCreateView.as_view(), name="ticket_create"),
]
