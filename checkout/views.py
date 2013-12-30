from django.shortcuts import render_to_response
from django.views.generic import ListView
from checkout.models import Equipment


def index(request):
    return render_to_response("checkout/index.html")


class EquipmentListView(ListView):
    model = Equipment
