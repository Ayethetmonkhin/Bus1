from django.contrib import admin
from .models import *
# Register your models here.
class busadmin(admin.ModelAdmin):
    list_display = ['id','bus_type','bus_number','operator']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(operator__user=request.user)


class SeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'seat_number', 'bus']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(bus__operator__user=request.user)

class BusRouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'bus']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(bus__operator__user=request.user)
    
class SeatBookAdmin(admin.ModelAdmin):
    list_display = ['id','route','bus_number','seat_number']

admin.site.register(Bus, busadmin)
admin.site.register(BusOperator)
admin.site.register(Route)
admin.site.register(Seat, SeatAdmin)
admin.site.register(BusRoute, BusRouteAdmin)
admin.site.register(SeatBooking)
admin.site.register(SeatBook, SeatBookAdmin)
