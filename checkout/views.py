from datetime import datetime
from django.contrib.auth.decorators import login_required
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

    def approve_reservation(self):
        self.model.is_approved = True

    def deny_reservation(self):
        self.model.is_approved = False


class FutureReservationListView(ListView):
    model = Reservation
    shows_all = False

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user, in_time__gte=datetime.now())


@login_required
def monitor_reservation_list(request):
    # TODO: We might want to have reservations stay on the list if they were that day
    reservations = Reservation.objects.filter(checked_in_time=None, is_approved=True)
    return render_to_response("checkout/monitor_reservation_list.html", {"reservations": reservations})


def reservation_detail(request, reservation_id=None):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render_to_response("checkout/reservation_detail.html",
                              {"reservation": reservation, "is_monitor": is_lab_monitor(request.user)})


def is_lab_monitor(user):
    return user.groups.filter(name='monitor')


@login_required
def monitor_checkout(request, reservation_id=None):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render_to_response("checkout/monitor_checkout.html", {"reservation": reservation})
