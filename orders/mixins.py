import csv

from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ExportAdminMixin:
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        metadata = self.model._meta
        filename = f"{metadata.model_name.lower()}_export_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
        field_names = [_.name for _ in metadata.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={filename}.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = _("Export selected as CSV")
