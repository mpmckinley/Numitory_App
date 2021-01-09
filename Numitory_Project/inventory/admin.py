from django.contrib import admin
from .models import Item, Type, Type_Detl, Collection

class InventoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Item, InventoryAdmin)

admin.site.register(Type, InventoryAdmin)
admin.site.register(Type_Detl, InventoryAdmin)

admin.site.register(Collection, InventoryAdmin)
