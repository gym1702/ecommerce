from django.contrib import admin
from .models import Categoria


class CategoriaAdmin(admin.ModelAdmin):

    #para el manejo del llenado automatico de slug
    prepopulated_fields = {'slug': ('nombre',)}
    

    list_display = ('nombre', 'descripcion', 'slug',)
    list_filter = ['nombre',]
    search_fields = ['nombre', 'descripcion',]


admin.site.register(Categoria, CategoriaAdmin)