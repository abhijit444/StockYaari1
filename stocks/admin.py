# admin.py
from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from .models import Index, DailyPrice

class DailyPriceResource(resources.ModelResource):
    class Meta:
        model = DailyPrice

class DailyPriceAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DailyPriceResource

# Don't register models here, it will be done in AppConfig.ready
admin.site.register(DailyPrice, DailyPriceAdmin)
admin.site.register(Index, DailyPriceAdmin)