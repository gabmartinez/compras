from django.contrib import admin

from orders.mixins import ExportAdminMixin
from orders.forms import ProviderForm, OrderForm
from orders.models import Provider, Department, Brand, UnitMeasure, Article, Order


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
    list_display = (
        "order_number",
        "order_date",
        "provider",
        "article",
        "quantity",
        "unit_measure",
    )
    search_fields = ("order_number",)
    list_filter = ("order_date", "provider", "article")
    ordering = ("-order_date",)
