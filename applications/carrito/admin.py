from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added',)
    search_fields = ['cart_id',]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'user',)
    search_fields = ['cart', 'product', 'user',]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)