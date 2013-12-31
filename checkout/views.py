from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import ListView
from checkout.models import Equipment


def index(request):
    return render_to_response("checkout/index.html")


class EquipmentListView(ListView):
    model = Equipment


def equipment_detail(request, equipment_id=None):
    equipment = get_object_or_404(Equipment, pk=equipment_id)
    return render_to_response("checkout/equipment_detail.html", {"equipment": equipment})
