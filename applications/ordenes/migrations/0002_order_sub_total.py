# Generated by Django 4.1.7 on 2023-04-04 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sub_total',
            field=models.FloatField(default=1, verbose_name='Subtotal'),
            preserve_default=False,
        ),
    ]