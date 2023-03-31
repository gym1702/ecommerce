from django.contrib import admin
from .models import Producto, Variante


class ProductoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

    list_display = ('nombre', 'precio', 'stock', 'categoria', 'fecha_edicion', 'disponible',)


class VarianteAdmin(admin.ModelAdmin):
    list_display = ('producto',  'variante_categoria', 'variante_valor', 'activo',)
    list_editable = ('activo',)
    list_filter = ('producto',  'variante_categoria', 'variante_valor', 'activo',)


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Variante, VarianteAdmin)