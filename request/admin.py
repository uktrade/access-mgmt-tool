from django.contrib import admin

from .models import AccessRequest

@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    readonly_fields = ("timestamp",)
    orderby = ("-timestamp", "-completed")
