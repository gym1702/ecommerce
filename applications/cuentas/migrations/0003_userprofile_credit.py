# Generated by Django 4.1.7 on 2023-04-07 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='credit',
            field=models.BooleanField(default=False, verbose_name='Tiene credito'),
        ),
    ]
