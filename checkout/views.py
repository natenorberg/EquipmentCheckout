from datetime import datetime
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView
from checkout.models import Equipment, Reservation


def is_admin(user):
    return user.is_superuser


def index(request):
    return render_to_response("checkout/index.html")


class EquipmentListView(ListView):
    model = Equipment


def equipment_detail(request, equipment_id=None):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    can_edit = is_admin(request.user)
    return render_to_response("checkout/equipment_detail.html", {"equipment": equipment, 'can_edit': can_edit},
                              context_instance=RequestContext(request))


@user_passes_test(is_admin)
def delete_equipment(request):
    if not request.POST:
        raise Http404
    equipment_id = request.POST['id']
    equipment = get_object_or_404(Equipment, id=equipment_id)
    equipment.delete()
    return HttpResponseRedirect("/checkout/equipment/")


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


def is_monitor(user):
    return user.groups.filter(name='Monitor') or user.is_superuser


@user_passes_test(is_monitor)
def monitor_reservation_list(request):
    # TODO: We might want to have reservations stay on the list if they were that day
    reservations = Reservation.objects.filter(checked_in_time=None, is_approved=True)
    return render_to_response("checkout/monitor_reservation_list.html", {"reservations": reservations})


def reservation_detail(request, reservation_id=None):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render_to_response("checkout/reservation_detail.html",
                              {"reservation": reservation, "is_monitor": is_monitor(request.user)})


@user_passes_test(is_monitor)
def monitor_checkout(request, reservation_id=None):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render_to_response("checkout/monitor_checkout.html", {"reservation": reservation},
                              context_instance=RequestContext(request))


@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    return render_to_response("auth/user_list.html", {'user_list': users},
                              context_instance=RequestContext(request))


@user_passes_test(is_admin)
def user_detail(request, user_id=None):
    # We can't pass in an object called 'user' or it will mess up the logout bar at the top
    user_object = get_object_or_404(User, pk=user_id)
    return render_to_response("auth/user_detail.html", {'user_object': user_object},
                              context_instance=RequestContext(request))

@user_passes_test(is_admin)
def delete_user(request):
    if not request.POST:
        raise Http404
    user_id = request.POST['id']
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return HttpResponseRedirect("/checkout/users/")