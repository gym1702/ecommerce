# Generated by Django 4.1.7 on 2023-03-25 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categorias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True, verbose_name='Producto')),
                ('slug', models.CharField(max_length=200, unique=True, verbose_name='Slug')),
                ('descripcion', models.TextField(blank=True, max_length=500, verbose_name='Descripcion')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Precio')),
                ('stock', models.IntegerField(verbose_name='Stock')),
                ('disponible', models.BooleanField(default=True, verbose_name='Disponible')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('fecha_edicion', models.DateTimeField(auto_now=True, verbose_name='Fecha de edicion')),
                ('imagen', models.ImageField(upload_to='fotos/productos', verbose_name='Imagen')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categorias.categoria')),
            ],
            options={
                'verbose_name_plural': 'Productos',
            },
        ),
    ]
