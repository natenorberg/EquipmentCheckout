from django.contrib import admin
from checkout.models import Equipment


class EquipmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['quantity']}),
        ('Date Information', {'fields': ['date_added'], 'classes': ['collapse']})
    ]
    list_display = ('name', 'date_added', 'quantity')
    list_filter = ['date_added']
    search_fields = ['name']


admin.site.register(Equipment, EquipmentAdmin)