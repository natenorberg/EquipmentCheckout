from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import ListView
from checkout.models import Equipment, Reservation


def index(request):
    return render_to_response("checkout/index.html")


class EquipmentListView(ListView):
    model = Equipment


def equipment_detail(request, equipment_id=None):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    return render_to_response("checkout/equipment_detail.html", {"equipment": equipment})


class ReservationListView(ListView):
    model = Reservation
    shows_all = True

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class FutureReservationListView(ListView):
    model = Reservation
    shows_all = False

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user, in_time__gte=datetime.now())


def reservation_detail(request, reservation_id=None):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render_to_response("checkout/reservation_detail.html", {"reservation": reservation})
