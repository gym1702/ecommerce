from django.db import models
from django.urls import reverse
from django.db.models import Avg, Count

from applications.categorias.models import Categoria
from applications.cuentas.models import Account



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


    #utilizado para enviar ruta de detalle de producto
    def get_url(self):
        return reverse('productos_app:producto_detalle', args=[self.categoria.slug, self.slug])
        #Genera una url: http://localhost:8000/tienda/categoria_slug/slug

    def __str__(self):
        return self.nombre
    

    def promedioReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(promedio=Avg('rating'))
        avg = 0
        if reviews['promedio'] is not None:
            avg = float(reviews['promedio'])
        return avg
    

    def contarReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(contar=Count('id'))
        contar = 0
        if reviews['contar'] is not None:
            contar = int(reviews['contar'])
        return contar

    
    class Meta:
        verbose_name_plural = 'Productos'
    



######## VARIANTES ##########

class VarienteManager(models.Manager):
    def colores(self):
        return super(VarienteManager, self).filter(variante_categoria='color', activo=True) 
    
    def tallas(self):
        return super(VarienteManager, self).filter(variante_categoria='talla', activo=True) 
    
variantes = (
    ('color', 'color'),
    ('talla', 'talla')
)

class Variante(models.Model):
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variante_categoria = models.CharField('Variantes', max_length=100, choices=variantes)
    variante_valor = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    objects = VarienteManager()

    def __str__(self):
        return self.variante_categoria +' : '+ self.variante_valor



######## COMENTARIOS ##########

class ReviewRating(models.Model):
    product = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Usuario')
    subject = models.CharField(max_length=100, blank=True, verbose_name='Titulo')
    review = models.CharField(max_length=500, blank=True, verbose_name='Comentario')
    rating = models.FloatField(verbose_name='Rating')
    ip = models.CharField(max_length=50, blank=True, verbose_name='Ip')
    status = models.BooleanField(default=True, verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de edicion')

    def __str__(self):
        return self.subject
    
    class Meta:
        verbose_name_plural = 'Comentarios'