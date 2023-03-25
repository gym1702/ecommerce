from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from applications.productos.models import Producto


def Home(request):

    productos = Producto.objects.filter(disponible=True)

    context = {
        'productos': productos
    }

    return render(request, 'home/home.html', context)
