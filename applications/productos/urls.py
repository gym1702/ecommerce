from django.urls import path

from . import views

app_name = 'productos_app'

urlpatterns = [
    path('tienda/', views.productos, name="productos"),
    path('tienda/<slug:categoria_slug>/', views.productos, name="productos_por_categoria"),
    path('tienda/<slug:categoria_slug>/<slug:producto_slug>/', views.producto_detalle, name="producto_detalle"),

]
