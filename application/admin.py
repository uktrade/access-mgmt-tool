from django.contrib import admin

from .models import Application, Integration


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass
