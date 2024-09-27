from django.contrib import admin
from .models import Equipment, Reservation, ReservationUser

# Equipmentモデルの管理画面設定
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number')
    search_fields = ('name', 'serial_number')

# Reservationモデルの管理画面設定
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'facility', 'formatted_start_time', 'formatted_end_time', 'user')
    list_filter = ('equipment', 'start_time', 'end_time')
    search_fields = ('equipment__name', 'facility', 'user__user__username')

    def formatted_start_time(self, obj):
        return obj.start_time.strftime('%H時')

    def formatted_end_time(self, obj):
        return obj.end_time.strftime('%H時')

    formatted_start_time.short_description = '開始時間'
    formatted_end_time.short_description = '終了時間'

# ReservationUserモデルの管理画面設定
@admin.register(ReservationUser)
class ReservationUserAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)