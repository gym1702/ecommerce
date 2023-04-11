from django.urls import path

from . import views

app_name = 'ordenes_app'

urlpatterns = [
    path('place_order/', views.place_order, name="place_order"),
    path('place_order_credit/', views.place_order_credit, name="place_order_credit"),
    path('payments/', views.payments, name="payments"),
    path('order_complete/', views.order_complete, name="order_complete"),

]
