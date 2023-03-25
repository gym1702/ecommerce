from django.db import models
from applications.categorias.models import Categoria



class Producto(models.Model):
    nombre = models.CharField('Producto', max_length=200, unique=True)
    slug = models.CharField('Slug', max_length=200, unique=True)
    descripcion = models.TextField('Descripcion', max_length=500, blank=True)
    precio = models.DecimalField('Precio', max_digits=6, decimal_places=2)
    stock = models.IntegerField('Stock')
    disponible = models.BooleanField('Disponible', default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField('Fecha de creacion', auto_now_add=True)
    fecha_edicion = models.DateTimeField('Fecha de edicion', auto_now =True)
    imagen = models.ImageField('Imagen', upload_to='fotos/productos')

    class Meta:
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre