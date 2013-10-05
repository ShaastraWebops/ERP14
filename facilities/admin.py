from django.contrib import admin
from facilities.models import FacilityItem, FacilityOrder, ItemEntry



admin.site.register(FacilityItem)

class ItemEntryInline(admin.TabularInline):
    model=ItemEntry

class FacilityOrderAdmin(admin.ModelAdmin):
    inlines=[ItemEntryInline, ]
    

admin.site.register(FacilityOrder, FacilityOrderAdmin)