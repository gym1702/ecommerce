# Generated by Django 4.1.7 on 2023-03-29 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_rename_vatiente_categoria_variante_variante_categoria'),
        ('carrito', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='productos.variante'),
        ),
    ]