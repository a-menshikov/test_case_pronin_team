from django.contrib import admin

from deals.models import Customer, Deal, Item


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Админ-панель модели покупателя."""

    list_display = ('id', 'login')
    ordering = ('id',)
    list_per_page = 50


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Админ-панель модели товара."""

    list_display = ('id', 'name')
    ordering = ('id',)
    list_per_page = 50


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    """Админ-панель модели сделки."""

    list_display = ('id', 'date', 'customer', 'item', 'total', 'quantity')
    list_filter = ('customer', 'item')
    list_per_page = 50
