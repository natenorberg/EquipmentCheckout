from datetime import datetime
from checkout.models import EquipmentReservation, Reservation


# Returns whether or not two reservations overlap
def overlap(reservation1, reservation2):
    if reservation1.out_time < reservation2.out_time:
        # First starts before second
        if reservation1.in_time < reservation2.out_time:
            return False  # First returned before second checked out. No overlap
        else:
            return True
    else:
        # Second reservation starts before first (since they're arbitrary)
        if reservation1.out_time > reservation2.in_time:
            return False  # Second is returned before first starts
        else:
            return True


# Finds conflicts between equipment from a reservation and list of equipment (assuming they overlap)
def conflicting_equipment(reservation1, reservation2):
    reservation1_equipment = EquipmentReservation.objects.filter(reservation=reservation1)
    reservation2_equipment = EquipmentReservation.objects.filter(reservation=reservation2)

    conflicts = []

    for item in reservation1_equipment:
        items_available = item.equipment.quantity - item.quantity
        for other_item in reservation2_equipment:
            if other_item.equipment.id == item.equipment.id:
                items_available -= other_item.quantity
                if items_available < 0:
                    if not item.equipment in conflicts:
                        conflicts.append(item.equipment)

    return conflicts


# Returns a list of conflicts that a reservation has
def detect_conflicts(reservation):
    other_reservations = Reservation.objects.exclude(pk=reservation.id)  # TODO: Make this more selective
    conflicts = []

    for other_reservation in other_reservations:
        if overlap(reservation, other_reservation):
            conflicts.extend(conflicting_equipment(other_reservation, reservation))

    return conflicts


# This is a simplified version of the Reservation class that only has these fields
# We need this because we want to check for conflicts as part of validation
class ReservationScheduleData():
    out_time = datetime
    in_time = datetime
    equipment = []

    def __init__(self, out_time, in_time, equipment):
        self.out_time = out_time
        self.in_time = in_time
        self.equipment = equipment