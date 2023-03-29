from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added',)
    search_fields = ['cart_id',]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity',)
    search_fields = ['cart', 'product',]



admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)