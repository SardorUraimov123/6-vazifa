from django.apps import apps
from django.contrib import admin
from .models import Product, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price'] 
    list_filter = ['name']  
    search_fields = ['name']  


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    readonly_fields = ['order_date']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [OrderInline]

    def get_ordering(self, request):
        return ['-order_date']

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.order_set.exists():
            return False
        return True

