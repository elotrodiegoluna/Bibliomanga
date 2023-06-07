# Generated by Django 4.2.1 on 2023-06-03 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_boleta_token_boleta_pagado_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanPremium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_plan', models.CharField(max_length=64, unique=True)),
                ('precio', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='premium',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Suscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.planpremium')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]