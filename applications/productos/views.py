from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages

from applications.categorias.models import Categoria
from applications.productos.models import Producto, ReviewRating
from applications.carrito.models import CartItem
from applications.carrito.views import _cart_id
from .forms import ReviewForm
from applications.ordenes.models import OrderProduct




#
def productos(request, categoria_slug=None):

    categorias = None
    productos = None   

    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)  
        productos = Producto.objects.filter(categoria=categorias, disponible=True) 

        #para paginacion
        paginator = Paginator(productos, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        ####

        contar_producto = productos.count() 

    else:
        categorias = Categoria.objects.all()
        productos = Producto.objects.filter(disponible=True)

        #para paginacion
        paginator = Paginator(productos, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        ###

        contar_producto = productos.count()

    context = {
        'categorias': categorias,
        #'productos': productos,
        'productos': paged_products,
        'contar_producto': contar_producto,
    }
    
    return render(request, 'productos/productos.html', context)


#
def producto_detalle(request, categoria_slug, producto_slug):
    try:
        producto_unico = Producto.objects.get(categoria__slug=categoria_slug, slug=producto_slug)
        #comprueba si el producto ya existe en carriro de compras
        in_cart =CartItem.objects.filter(cart__cart_id = _cart_id(request), product = producto_unico).exists()

    except Exception as e:
        raise e

    #Validar que el usuario compro el producto para poder enviar comentarios
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=producto_unico.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

        
    #Mostrar comentarios del producto en el template
    reviews = ReviewRating.objects.filter(product_id=producto_unico.id, status=True)
    

    context = {
        'producto_unico': producto_unico,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
    }

    return render(request, 'productos/producto_detalle.html', context)


#
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            productos = Producto.objects.order_by('-fecha_creacion').filter(Q(descripcion__icontains=keyword) | Q(nombre__icontains=keyword))
            product_count = productos.count()

    context = {
        'productos': productos,
        'contar_producto': product_count,
    }

    return render(request, 'productos/productos.html', context)



#
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Muchas gracias!, su comentario ha sido actualizado.')
            return redirect(url)
        
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Muchas gracias!, su comentario ha sido enviado con éxito.')
                return redirect(url)


