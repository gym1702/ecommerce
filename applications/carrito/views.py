from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


from applications.productos.models import Producto, Variante
from .models import Cart, CartItem


#Funcuion que entrega la sesion del usuario actual
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request, product_id):
    #necesario crea carrito de compra y agregar variantes
    product = Producto.objects.get(id = product_id)

    #para agregar variantes
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variante.objects.get(producto = product, variante_categoria__iexact = key, variante_valor__iexact = value)
                product_variation.append(variation)
            except:
                pass


    #crea carrito de compra
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()


    #revisa si existen items con varientes iguales
    is_cart_item_exist = CartItem.objects.filter(product = product, cart = cart).exists()

    #aumenta cantidad de producto en carrito existente o crea items
    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product = product, cart = cart)

        #para conocer las variantes de cada producto
        ex_var_list = []
        id = []

        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product = product, id = item_id)
            item.quantity += 1
            item.save()
        
        else:
            item = CartItem.objects.create(product = product, quantity = 1,  cart = cart)
            #inserta cada variante
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)

            item.save()

    #crea carrito desde cero
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )

        #inserta cada variante
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)

        #guarda items agregados
        cart_item.save()
    
    return redirect('carrito_app:carrito')



def remove_cart(request, product_id, cart_item_id):
    #disminuye cantidad de producto en carrito
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Producto, id = product_id)

    try:    
        cart_item = CartItem.objects.get(product = product, cart = cart, id = cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    
    return redirect('carrito_app:carrito')



def remove_cart_item(request, product_id, cart_item_id):
    #Elimina todo el item del carrito
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Producto, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart, id = cart_item_id)

    cart_item.delete()

    return redirect('carrito_app:carrito')



def cart(request, total=0, quantity=0, cart_items=None):
    iva = 0
    subtotal = 0

    #agrega los datos al template del carrito de compras
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items =CartItem.objects.filter(cart = cart, is_active = True).order_by('id')

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
