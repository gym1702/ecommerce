from django.db import models

from applications.productos.models import Producto



class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
    class Meta:
        verbose_name_plural = 'Carritos'


class CartItem(models.Model):
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    ##Para calcular precio total por producto en template
    def subtotal(self):
        return self.product.precio * self.quantity
    
    

    def __str__(self):
        return str(self.product)
    
    class Meta:
        verbose_name_plural = 'Carritos_Detalles'


