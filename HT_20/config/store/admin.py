from django.contrib import admin

from store.models import Category, Product, Cart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass
