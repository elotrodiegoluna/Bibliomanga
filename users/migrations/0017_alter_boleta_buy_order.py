# Generated by Django 4.2.1 on 2023-06-12 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_pedido_apellido_receptor_alter_pedido_comuna_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boleta',
            name='buy_order',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
