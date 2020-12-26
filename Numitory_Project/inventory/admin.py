from django.contrib import admin
from .models import Item, Type, Collection

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Item, TodoAdmin)

admin.site.register(Type, TodoAdmin)

admin.site.register(Collection, TodoAdmin)