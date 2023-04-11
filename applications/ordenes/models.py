from django.db import models

from applications.cuentas.models import Account
from applications.productos.models import Producto, Variante


#
class Payment(models.Model):
    metodo_pago =(
        ('Credito', 'Credito'),
        ('Contado', 'Contado'),
        ('Paypal', 'Paypal'),
        ('Tarjeta', 'Tarjeta'),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Usuario')
    payment_id = models.CharField(max_length=100, verbose_name='Pago_id')
    payment_method = models.CharField(max_length=100, choices=metodo_pago, default='Contado', verbose_name='Metodo de pago')
    amount_id = models.CharField(max_length=100, verbose_name='Monto a pagar')
    status = models.CharField(max_length=100, verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')

    def __str__(self):
        return self.payment_id
    
    class Meta:
        verbose_name_plural = 'Pagos'


#
class Order(models.Model):
    STATUS =(
        ('Nuevo', 'Nuevo'),
        ('Aceptado', 'Aceptado'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado')
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True,  verbose_name='Usuario')
    pyment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Pago')
    order_number = models.CharField(max_length=20, verbose_name='Numero de orden')
    first_name = models.CharField(max_length=50, verbose_name='Nombre(s)')
    last_name = models.CharField(max_length=50, verbose_name='Apellido(s)')
    phone = models.CharField(max_length=10, verbose_name='Telefono')
    email = models.CharField(max_length=100, verbose_name='Email')
    addres_line_1 = models.CharField(max_length=100, verbose_name='Direccion')
    addres_line_2 = models.CharField(max_length=100, verbose_name='Direccion_2')
    city = models.CharField(max_length=100, verbose_name='Ciudad')
    state = models.CharField(max_length=50, verbose_name='Estado')
    country = models.CharField(max_length=50, verbose_name='Pais')
    order_note = models.CharField(max_length=150, verbose_name='Descripcion o referencia', blank=True)
    sub_total = models.FloatField(verbose_name='Subtotal')
    tax = models.FloatField(verbose_name='IVA')
    order_total = models.FloatField(verbose_name='Total')
    status = models.CharField(max_length=20, verbose_name='Status', choices=STATUS, default='Nuevo')
    ip = models.CharField(max_length=50, blank=True, verbose_name='Ip')
    is_ordered = models.BooleanField(default=False, verbose_name='Ya ordenado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de edicion')

    def __str__(self):
        return self.first_name +' '+ self.last_name
    
    def full_address(self):
        return self.addres_line_1 +', '+ self.addres_line_2
    
    def full_name(self):
        return self.first_name +' '+ self.last_name

    
    class Meta:
        verbose_name_plural = 'Ordenes de compra'


#
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Orden')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Pago')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Usuario')
    product = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    variation = models.ManyToManyField(Variante, blank=True, verbose_name='Variante')
    quantity = models.IntegerField(verbose_name='Cantidad')
    product_price = models.FloatField(verbose_name='Precio')
    ordered = models.BooleanField(default=False, verbose_name='Ya ordenado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de edicion')

    def __str__(self):
        return self.product.nombre
    
    class Meta:
        verbose_name_plural = 'Productos en ordenes'



#
# class Credit(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, verbose_name='Orden')
#     user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, verbose_name='Usuario')
#     amount = models.CharField(max_length=100, verbose_name='Monto a pagar')
#     status = models.CharField(max_length=100, verbose_name='Status')
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')



# #
# class CreditPayment(models.Model):
#     credit = models.ForeignKey(Credit, on_delete=models.CASCADE,)
#     user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, verbose_name='Usuario')
#     credit_amount = models.CharField(max_length=100, verbose_name='Monto del credito')
#     payment = models.FloatField(verbose_name='Pago')
#     date_payment = models.DateTimeField(auto_now=True, verbose_name='Fecha de pago')