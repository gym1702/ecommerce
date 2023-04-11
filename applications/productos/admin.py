from django.contrib import admin
import admin_thumbnails #(Para esta libreria inatalar django-admin-thumbnails)
from .models import Producto, Variante, ReviewRating, ProductGallery


@admin_thumbnails.thumbnail('image')
class ProductGalleryInLine(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}
    list_display = ('nombre', 'precio', 'stock', 'categoria', 'fecha_edicion', 'disponible',)
    inlines = [ProductGalleryInLine]


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
admin.site.register(ProductGallery)