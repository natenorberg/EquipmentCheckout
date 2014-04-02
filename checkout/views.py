from datetime import datetime
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import ListView
from checkout.mediator import detect_conflicts
from checkout.models import Equipment, Reservation, EquipmentReservation, SubItem


def is_admin(user):
    return user.is_superuser


def index(request):
    return render_to_response("checkout/index.html")


class EquipmentListView(ListView):
    model = Equipment
    equipment_tab = True


def equipment_detail(request, equipment_id=None):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    sub_items = SubItem.objects.filter(kit=equipment_id)
    can_edit = is_admin(request.user)
    return render_to_response("checkout/equipment_detail.html",
                              {"equipment": equipment, 'can_edit': can_edit, 'sub_items': sub_items,
                               'equipment_tab': True},
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
    reservation_tab = True

    def get_queryset(self):
        # Admins should be able to see all reservations so that they can approve them
        if is_admin(self.request.user):
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)

    def approve_reservation(self):
        self.model.is_approved = True

    def deny_reservation(self):
        self.model.is_approved = False


class FutureReservationListView(ListView):
    model = Reservation
    shows_all = False
    reservation_tab = True

    def get_queryset(self):
        if is_admin(self.request.user):
            return Reservation.objects.filter(in_time__gte=datetime.now())
        return Reservation.objects.filter(user=self.request.user, in_time__gte=datetime.now())


def is_monitor(user):
    return user.groups.filter(name='Monitor') or user.is_superuser


@user_passes_test(is_monitor)
def monitor_reservation_list(request):
    # TODO: We might want to have reservations stay on the list if they were that day
    reservations = Reservation.objects.filter(checked_in_time=None, is_approved=True)
    return render_to_response("checkout/monitor_reservation_list.html",
                              dict(reservations=reservations, monitor_tab=True),
                              context_instance=RequestContext(request))


@login_required
def reservation_detail(request, reservation_id=None):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    equipment = EquipmentReservation.objects.filter(reservation=reservation)

    return render_to_response("checkout/reservation_detail.html",
                              dict(reservation=reservation, equipment=equipment, is_monitor=is_monitor(request.user),
                                   reservation_tab=True),
                              context_instance=RequestContext(request))


@login_required
def reservation_conflicts(request, reservation_id=None):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    conflicts = detect_conflicts(reservation)
    return render_to_response("checkout/reservation_conflicts.html",
                              {'reservation': reservation, 'conflicts': conflicts, 'reservation_tab': True},
                              context_instance=RequestContext(request))


@login_required
def delete_reservation(request):
    if not request.POST:
        raise Http404
    reservation_id = request.POST['id']
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.user != reservation.user and not request.user.is_superuser:
        raise Http404  # TODO: Create permission denied page
    reservation.delete()
    return HttpResponseRedirect("/checkout/reservations")


@user_passes_test(is_admin)
def approve_reservation(request):
    if not request.POST:
        raise Http404
    reservation_id = request.POST['id']
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.is_approved = True
    reservation.save()
    return HttpResponseRedirect("/checkout/reservations/")


@user_passes_test(is_admin)
def reject_reservation(request):
    if not request.POST:
        raise Http404
    reservation_id = request.POST['id']
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.is_approved = False
    reservation.save()
    return HttpResponseRedirect("/checkout/reservations/")


def get_selected_kits(reservation):
    selected_kits = []
    for item in EquipmentReservation.objects.filter(reservation=reservation):
        if item.equipment.is_kit:
            selected_kits.append(item.equipment)

    return selected_kits

@user_passes_test(is_monitor)
def monitor_checkout(request, reservation_id=None):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    equipment = EquipmentReservation.objects.filter(reservation=reservation)
    has_kits = False
    if get_selected_kits(reservation).__len__() > 0:
        has_kits = True
    return render_to_response("checkout/monitor_checkout.html",
                              {"reservation": reservation, 'equipment': equipment, 'has_kits': has_kits,
                               'monitor_tab': True},
                              context_instance=RequestContext(request))


@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    return render_to_response("auth/user_list.html", {'user_list': users, 'users_tab': True},
                              context_instance=RequestContext(request))


@user_passes_test(is_admin)
def user_detail(request, user_id=None):
    # We can't pass in an object called 'user' or it will mess up the logout bar at the top
    user_object = get_object_or_404(User, pk=user_id)
    return render_to_response("auth/user_detail.html", {'user_object': user_object, 'users_tab': True},
                              context_instance=RequestContext(request))


@user_passes_test(is_admin)
def delete_user(request):
    if not request.POST:
        raise Http404
    user_id = request.POST['id']
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return HttpResponseRedirect("/checkout/users/")