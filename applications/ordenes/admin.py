from django.contrib import admin
from .models import Payment, Order, OrderProduct


#Para mostrar tabla de productos relacionados a una orden de compra
class OrderProductInLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0



class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 
                    'status', 'is_ordered', 'created_at',]
    list_filter = ['status', 'is_ordered',]
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email',]
    list_per_page = 20
    inlines = [OrderProductInLine]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'user', 'payment_method', 'amount_id', 'created_at', 'status', ]



admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
