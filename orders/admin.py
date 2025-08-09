import requests
from daterangefilter.filters import PastDateRangeFilter
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth import get_permission_codename
from django.utils.translation import gettext as _

from orders.mixins import ExportAdminMixin
from orders.forms import ProviderForm, OrderForm
from orders.models import (
    Provider,
    Department,
    Brand,
    UnitMeasure,
    Article,
    Order,
    UnpublishedOrder,
)


@admin.register(Department)
class DepartmentAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Brand)
class BrandAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ("description", "is_active")
    search_fields = ("description",)
    list_filter = ("is_active",)


@admin.register(UnitMeasure)
class UnitMeasureAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ("description", "is_active")
    search_fields = ("description",)
    list_filter = ("is_active",)


@admin.register(Provider)
class ProviderAdmin(ExportAdminMixin, admin.ModelAdmin):
    form = ProviderForm
    list_display = (
        "name",
        "person_type",
        "document_number",
        "is_active",
    )
    search_fields = ("name", "document_number")
    list_filter = ("is_active", "person_type")


@admin.register(Article)
class ArticleAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ("description", "brand", "unit_measure", "stock", "is_active")
    search_fields = ("description",)
    list_filter = ("brand", "unit_measure", "is_active")
    ordering = ("description",)


@admin.register(Order)
class OrderAdmin(ExportAdminMixin, admin.ModelAdmin):
    form = OrderForm
    list_display_links = ("order_number",)
    list_display = (
        "accounting_entry_number",
        "order_number",
        "order_date",
        "provider",
        "article",
        "quantity",
        "unit_measure",
    )
    search_fields = ("order_number", "accounting_entry_number")
    list_filter = (("order_date", PastDateRangeFilter), "provider", "article")
    ordering = ("-order_date",)


@admin.register(UnpublishedOrder)
class UnpublishedOrderAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = (
        "order_number",
        "order_date",
        "provider",
        "article",
        "quantity",
        "unit_measure",
    )
    search_fields = ("order_number",)
    list_filter = (("order_date", PastDateRangeFilter), "provider", "article")
    ordering = ("-order_date",)
    actions = ["publish_to_accounting_action"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return (
            super().get_queryset(request).filter(accounting_entry_number__isnull=True)
        )

    def has_publish_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("change", opts)
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    @admin.action(
        description=_("Publish selected Orders to Accounting System"),
        permissions=["publish"],
    )
    def publish_to_accounting_action(self, request, queryset):
        headers = {
            "x-api-key": settings.ACCOUNTING_API_KEY,
            "Content-Type": "application/json",
        }
        success, failed = 0, 0
        for order in queryset:
            data = {
                "descripcion": f"Order #{order.order_number}",
                "cuenta_Id": settings.ACCOUNTING_ACCOUNT_ID,
                "auxiliar_Id": settings.ACCOUNTING_AUXILIARY_ID,
                "tipoMovimiento": settings.ACCOUNTING_MOVEMENT_TYPE,
                "fechaAsiento": str(order.order_date),
                "montoAsiento": str(round(order.total_price, 2)),
            }
            response = requests.post(
                settings.ACCOUNTING_SERVICE_URL, json=data, headers=headers
            )
            if response.status_code != 201:
                failed += 1
                continue

            response_data = response.json()
            if not response_data.get("success", False):
                failed += 1
                continue

            entry_number = response_data.get("data", {}).get("id", None)
            if not entry_number:
                failed += 1
                continue
            order.accounting_entry_number = entry_number
            order.save(update_fields=["accounting_entry_number"])
            success += 1

        if success > 0:
            messages.success(
                request,
                _(
                    "{count} orders successfully published to the accounting system."
                ).format(count=success),
            )

        if failed > 0:
            messages.error(
                request,
                _("{count} orders failed to publish to the accounting system.").format(
                    count=failed
                ),
            )
