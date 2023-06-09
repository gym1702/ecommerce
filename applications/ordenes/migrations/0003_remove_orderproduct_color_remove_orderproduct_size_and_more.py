# Generated by Django 4.1.7 on 2023-04-05 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_rename_vatiente_categoria_variante_variante_categoria'),
        ('ordenes', '0002_order_sub_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
        migrations.AlterField(
            model_name='order',
            name='is_ordered',
            field=models.BooleanField(default=False, verbose_name='Ya ordenado'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=10, verbose_name='Telefono'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='ordered',
            field=models.BooleanField(default=False, verbose_name='Ya ordenado'),
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='variation',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variation',
            field=models.ManyToManyField(blank=True, to='productos.variante', verbose_name='Variante'),
        ),
    ]
