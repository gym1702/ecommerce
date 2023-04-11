from django.shortcuts import render,redirect
import datetime
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse

from applications.carrito.models import CartItem
from .models import Order, Payment, OrderProduct

from .forms import OrderForm

from applications.productos.models import Producto
from applications.cuentas.models import UserProfile



#
def payments(request):
    #Crea registro en tabla payment
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_id = order.order_total,
        status = body['status'],
    )
    payment.save()

    #Actualiza tabla order
    order.pyment = payment
    order.is_ordered = True
    order.save()

    #Registrar dentro de la tabla Order todo el carrito de compras
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.precio
        orderproduct.ordered = True
        orderproduct.save()

        #almacenar las variantes
        cart_item =  CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

        #Actualizar stok de productos
        product = Producto.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()


    #Eliminar carrito de compras una vez hecha toda la transaccion
    CartItem.objects.filter(user=request.user).delete()

    #Enviar email de confitmacion de pedido
    mail_subject = 'Gracias por su compra'
    body = render_to_string('ordenes/recibe_email_orden.html', {
        'user': request.user,
        'order': order,
    })

    to_mail = request.user.email
    send_email = EmailMessage(mail_subject, body, to=[to_mail])
    send_email.send()    

    #Enviar data a template orden comletada
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,    
    }  
        
    return JsonResponse(data)
    # return render(request, 'ordenes/pagos.html')



#
#ORDENAR PRODUCTOS SIN CREDITO
def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('productos_app:productos')
    
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.precio * cart_item.quantity)
        quantity += cart_item.quantity

    
    grand_total = total
    sub = float(total) / float(1.16)
    tax = float(total) - float(sub)
    sub_total = float(total) - float(tax)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.addres_line_1 = form.cleaned_data['addres_line_1']
            data.addres_line_2 = form.cleaned_data['addres_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.sub_total = sub_total
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))

            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)

            data.order_number = order_number
            data.save()

            #Data para llenado de template payments
            order = Order.objects.get(user = current_user, is_ordered = False, order_number = order_number)
            
            context = {
                'order': order,
                'cart_items': cart_items,
                'subtotal' : sub_total,
                'iva': tax,
                'total': grand_total,
            }

            return render(request, 'ordenes/pagos.html', context)
    
    else:
        return redirect('carrito_app:checkout')



#ORDENAR PRODUCTOS A CREDITO
def place_order_credit(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('productos_app:productos')
    
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.precio * cart_item.quantity)
        quantity += cart_item.quantity

    
    grand_total = total
    sub = float(total) / float(1.16)
    tax = float(total) - float(sub)
    sub_total = float(total) - float(tax)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.addres_line_1 = form.cleaned_data['addres_line_1']
            data.addres_line_2 = form.cleaned_data['addres_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.sub_total = sub_total
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))

            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)

            data.order_number = order_number
            data.save()
            

            

            #Data para llenado de template payments
            order = Order.objects.get(user = current_user, is_ordered = False, order_number = order_number)
            credit = UserProfile.objects.get(user = current_user, credit=True)

            #Cambia el estado de is ordered
            order.is_ordered = True
            order.save()

            
            #Registrar dentro de la tabla Order todo el carrito de compras
            cart_items = CartItem.objects.filter(user=request.user)

            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                #orderproduct.payment = ''
                orderproduct.user_id = request.user.id
                orderproduct.product_id = item.product_id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.precio
                orderproduct.ordered = True
                orderproduct.save()

                #almacenar las variantes
                cart_item =  CartItem.objects.get(id=item.id)
                product_variation = cart_item.variations.all()
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                orderproduct.variation.set(product_variation)
                orderproduct.save()

                #Actualizar stok de productos
                product = Producto.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()


            #Eliminar carrito de compras una vez hecha toda la transaccion
            CartItem.objects.filter(user=request.user).delete()

            #Enviar email de confitmacion de pedido
            mail_subject = 'Gracias por su compra'
            body = render_to_string('ordenes/recibe_email_orden.html', {
                'user': request.user,
                'order': order,
            })

            to_mail = request.user.email
            send_email = EmailMessage(mail_subject, body, to=[to_mail])
            send_email.send()    
            
            context = {
                'order': order,
                'cart_items': cart_items,
                'subtotal' : sub_total,
                'iva': tax,
                'total': grand_total,
                'credit': credit,
                'order_number': order.order_number,
            }

            return render(request, 'ordenes/orden_completa_credito.html', context)
    
    else:
        return redirect('carrito_app:checkout')



#
def order_complete(request):
    #manda data a orden completa
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        importe = 0

        for i in ordered_products:
            importe += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'importe': importe,
            'subtotal': order.sub_total
        }

        return render(request, 'ordenes/orden_completa.html', context)
    
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home_app:home')



