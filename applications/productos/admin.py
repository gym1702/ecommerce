from django.contrib import admin
from .models import Producto, Variante, ReviewRating


class ProductoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

    list_display = ('nombre', 'precio', 'stock', 'categoria', 'fecha_edicion', 'disponible',)


class VarianteAdmin(admin.ModelAdmin):
    list_display = ('producto',  'variante_categoria', 'variante_valor', 'activo',)
    list_editable = ('activo',)
    list_filter = ('producto',  'variante_categoria', 'variante_valor', 'activo',)


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('subject', 'review', 'product', 'rating', 'status', 'user',)
    search_fields = ('product', 'status',)
    list_filter = ('status',)


admin.site.register(Producto, ProductoAdmin)
admin.site.register(Variante, VarianteAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)