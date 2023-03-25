from django.contrib import admin
from .models import Producto


class ProductoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

    list_display = ('nombre', 'precio', 'stock', 'categoria', 'fecha_edicion', 'disponible',)


admin.site.register(Producto, ProductoAdmin)