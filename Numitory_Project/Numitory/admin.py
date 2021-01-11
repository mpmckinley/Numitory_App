from django.contrib import admin
from inventory.models import Transaction, Type, Collection, Item, UserExtended, MetalPrices

admin.site.register(Transaction)
admin.site.register(Type)
admin.site.register(Collection)
admin.site.register(Item)
admin.site.register(UserExtended)
admin.site.register(MetalPrices)