from import_export import resources
from .models import DailyPrice

class DailyPriceResource(resources.ModelResource):
    class Meta:
        model = DailyPrice