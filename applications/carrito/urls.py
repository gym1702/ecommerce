from django.urls import path

from . import views

app_name = 'carrito_app'

urlpatterns = [
    path('carrito/', views.cart, name="carrito"),
    path('carrito/agregar/<int:product_id>/', views.add_cart, name="agregar_carrito"),
    path('carrito/eliminar/<int:product_id>/', views.remove_cart, name="eliminar_carrito"),
    path('carrito/eliminar_item/<int:product_id>/', views.remove_cart_item, name="eliminar_carrito_item"),

]
