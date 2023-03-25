from django.shortcuts import render, get_object_or_404

from applications.categorias.models import Categoria
from applications.productos.models import Producto


def productos(request, categoria_slug=None):

    categorias = None
    productos = None   

    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)  
        productos = Producto.objects.filter(categoria=categorias, disponible=True) 
        contar_producto = productos.count() 

    else:
        categorias = Categoria.objects.all()
        productos = Producto.objects.filter(disponible=True)
        contar_producto = productos.count()

    context = {
        'categorias': categorias,
        'productos': productos,
        'contar_producto': contar_producto,
    }

    
    return render(request, 'productos/productos.html', context)



def producto_detalle(request, categoria_slug, producto_slug):

    try:
        producto_unico = Producto.objects.get(categoria__slug=categoria_slug, slug=producto_slug)

    except Exception as e:
        raise e
    
    context = {
        'producto_unico': producto_unico,
    }

    return render(request, 'productos/producto_detalle.html', context)
