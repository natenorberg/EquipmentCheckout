from datetime import datetime
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import SplitDateTimeWidget
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from checkout.models import Reservation, Equipment
from checkout.views import is_monitor, is_admin


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment

    def clean(self):
        cleaned_data = super(EquipmentForm, self).clean()
        quantity = cleaned_data.get('quantity')

        if not quantity > 0:
            message = "Quantity must be greater than zero"
            if not 'quantity' in self._errors:
                from django.forms.util import ErrorList

                self._errors['quantity'] = ErrorList()
            self._errors['quantity'].append(message)

        return cleaned_data


@user_passes_test(is_admin)
def new_equipment(request):
    title = "New Equipment"
    if request.POST:
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/checkout/equipment/')
    else:
        form = EquipmentForm()
    return render_to_response("checkout/equipment_edit.html", {'form': form, 'title': title},
                              context_instance=RequestContext(request))


@user_passes_test(is_admin)
def edit_equipment(request, equipment_id):
    instance = get_object_or_404(Equipment, id=equipment_id)
    title = "Edit Equipment"
    form = EquipmentForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect('/checkout/equipment/')
    return render_to_response("checkout/equipment_edit.html", {'form': form, 'title': title},
                              context_instance=RequestContext(request))


class ReservationForm(forms.ModelForm):
    equipment = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'equipment_list'}),
                                               queryset=Equipment.objects.all())
    out_time = forms.DateTimeField(widget=SplitDateTimeWidget())
    in_time = forms.DateTimeField(widget=SplitDateTimeWidget())
    error_css_class = 'error'

    class Meta:
        model = Reservation
        fields = ['project', 'equipment', 'out_time', 'in_time']

    def clean(self):
        cleaned_data = super(ReservationForm, self).clean()
        check_out_time = cleaned_data.get("out_time")
        check_in_time = cleaned_data.get("in_time")

        if check_out_time and check_in_time:
            if check_out_time > check_in_time:
                message = "Check in time must be later than check out time."
                if not 'in_time' in self._errors:
                    from django.forms.util import ErrorList

                    self._errors['in_time'] = ErrorList()
                self._errors['in_time'].append(message)

        return cleaned_data


@login_required
def new_reservation(request):
    if request.POST:
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.is_approved = False
            form.save()
            return HttpResponseRedirect('/checkout/reservations')
    else:
        form = ReservationForm()
    return render_to_response("checkout/reservation_edit.html", {'form': form},
                              context_instance=RequestContext(request))


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_out_comments']


class CheckInForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_in_comments']


@user_passes_test(is_monitor)
def check_out_comments(request):
    if not request.POST:
        raise Http404
    pk = request.POST['id']
    instance = get_object_or_404(Reservation, id=pk)
    form = CheckoutForm(request.POST or None, instance=instance)
    page_title = "Equipment Check Out"
    if request.POST.get('edited') and form.is_valid():
        form.instance.checked_out_by = request.user
        form.instance.checked_out_time = datetime.now()
        form.save()
        return HttpResponseRedirect('/checkout/monitor')
    return render_to_response("checkout/checkout_comments.html",
                              {'form': form, 'reservation': instance, 'page_title': page_title},
                              context_instance=RequestContext(request), )


@user_passes_test(is_monitor)
def check_in_comments(request):
    if not request.POST:
        raise Http404
    pk = request.POST['id']
    instance = get_object_or_404(Reservation, id=pk)
    form = CheckInForm(request.POST or None, instance=instance)
    page_title = "Equipment Check In"
    if request.POST.get('edited') and form.is_valid():
        form.instance.checked_in_by = request.user
        form.instance.checked_in_time = datetime.now()
        form.save()
        return HttpResponseRedirect('/checkout/monitor')
    return render_to_response("checkout/checkout_comments.html",
                              {'form': form, 'reservation': instance, 'page_title': page_title},
                              context_instance=RequestContext(request), )
