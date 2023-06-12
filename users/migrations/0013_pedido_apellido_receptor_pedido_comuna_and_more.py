# Generated by Django 4.2.1 on 2023-06-11 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_estadopedido_tipoentrega_boleta_buy_order_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='apellido_receptor',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='comuna',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='direccion',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='n_depto',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='nombre_receptor',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='pedido',
            name='telefono',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='tipo_entrega',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.DeleteModel(
            name='EstadoPedido',
        ),
        migrations.DeleteModel(
            name='TipoEntrega',
        ),
    ]
