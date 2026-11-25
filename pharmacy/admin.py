from django.contrib import admin
from .models import Category, Medicine, Customer, Sale, SaleItem

admin.site.register(Category)
admin.site.register(Medicine)
admin.site.register(Customer)
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "sale_date", "total_amount")
    inlines = [SaleItemInline]
