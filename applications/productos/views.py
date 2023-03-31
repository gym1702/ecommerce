from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from applications.categorias.models import Categoria
from applications.productos.models import Producto
from applications.carrito.models import CartItem
from applications.carrito.views import _cart_id





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



def producto_detalle(request, categoria_slug, producto_slug):
    try:
        producto_unico = Producto.objects.get(categoria__slug=categoria_slug, slug=producto_slug)
        #comprueba si el producto ya existe en carriro de compras
        in_cart =CartItem.objects.filter(cart__cart_id = _cart_id(request), product = producto_unico).exists()

    except Exception as e:
        raise e
    
    context = {
        'producto_unico': producto_unico,
        'in_cart': in_cart,
    }

    return render(request, 'productos/producto_detalle.html', context)



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



