# Generated by Django 5.1.5 on 2025-01-18 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mi_negocio', '0003_tienda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
