# Generated by Django 4.2.1 on 2023-06-26 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_review_listafavorito_listadeseados_itemfavorito_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listadeseados',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]