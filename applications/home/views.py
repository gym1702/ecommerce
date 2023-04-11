from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from applications.productos.models import Producto, ReviewRating


def Home(request):

    productos = Producto.objects.filter(disponible=True).order_by('fecha_creacion')

    for producto in productos:
        reviews = ReviewRating.objects.filter(product_id=producto.id, status=True)

    context = {
        'productos': productos,
        'reviews': reviews,
    }

    return render(request, 'home/home.html', context)
