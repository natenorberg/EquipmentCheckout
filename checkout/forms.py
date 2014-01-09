from django import forms
from django.contrib.auth.decorators import login_required
from django.forms import SplitDateTimeWidget
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from checkout.models import Reservation, Equipment


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
                #raise forms.ValidationError("Check in time must be later than check out time.")
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
            new_reservation = form.save()
            return HttpResponseRedirect('/checkout/reservations')
    else:
        form = ReservationForm()
    return render_to_response("checkout/reservation_add.html", {'form': form}, context_instance=RequestContext(request))