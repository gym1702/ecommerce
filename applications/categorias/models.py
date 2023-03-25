from django.db import models
from django.urls import reverse



class Categoria(models.Model):
    nombre = models.CharField('Nombre', max_length=50, unique=True,)
    descripcion = models.CharField('Descripcion', max_length=255, blank=True)
    slug = models.CharField('Slug', max_length=100, unique=True)
    imagen = models.ImageField('Imagen', upload_to='fotos/categorias', blank=True)


    #utilizado para enviar ruta de categorias en el navbar
    def get_url(self):
        return reverse('productos_app:productos_por_categoria', args=[self.slug])
        #Genera una url: http://localhost:8000/tienda/slug

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorias" 