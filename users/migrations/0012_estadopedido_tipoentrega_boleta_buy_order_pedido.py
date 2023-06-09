# Generated by Django 4.2.1 on 2023-06-10 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_mangaleido'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoEntrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='boleta',
            name='buy_order',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boleta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.boleta')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.estadopedido')),
                ('tipo_entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.tipoentrega')),
            ],
        ),
    ]
