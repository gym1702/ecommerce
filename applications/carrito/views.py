from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


from applications.productos.models import Producto
from .models import Cart, CartItem


#Funcuion que entrega la sesion del usuario actual
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request, product_id):
    #crea carrito de compra
    product = Producto.objects.get(id = product_id)
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    #aumenta cantidad de producto en carrito
    try:
        cart_item = CartItem.objects.get(product = product, cart = cart)
        cart_item.quantity += 1 
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    
    return redirect('carrito_app:carrito')



def remove_cart(request, product_id):
    #disminuye cantidad de producto en carrito
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Producto, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('carrito_app:carrito')



def remove_cart_item(request, product_id):
    #Elimina todo el item del carrito
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Producto, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)

    cart_item.delete()

    return redirect('carrito_app:carrito')



def cart(request, total=0, quantity=0, cart_items=None):
    #agrega los datos al template del carrito de compras
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items =CartItem.objects.filter(cart = cart, is_active = True)

        #para saber el precio total de los productos y cantidad de productos en carrito
        for cart_item in cart_items:
            total += (cart_item.product.precio * cart_item.quantity)
            quantity += cart_item.quantity
        
        ##Para calcular precio mas iva
        #iva = (16 * total)/100
        #grantotal = total + iva

        ##Para calcular precio con iva incluido
        subtotal = float(total) / float(1.16)
        iva = float(total) - float(subtotal)

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'iva': iva,
        'subtotal': subtotal,
        #'grantotal': grantotal,
    }


    return render(request, 'carrito/carrito.html', context)
