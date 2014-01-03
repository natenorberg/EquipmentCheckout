from django.contrib import admin
from checkout.models import Equipment, Reservation


class EquipmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['quantity']}),
        (None, {'fields': ['condition']}),
        (None, {'fields': ['description']}),
        ('Permissions', {'fields': ['music_ed', 'pre_gate', 'post_gate', 'staff']})
    ]
    list_display = ('name', 'date_added', 'quantity', 'condition')
    list_filter = ['date_added']
    search_fields = ['name']


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'out_time', 'in_time')


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Reservation, ReservationAdmin)