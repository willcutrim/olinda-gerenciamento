# Generated by Django 4.1.2 on 2023-08-22 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caixa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrinho',
            name='produtos',
            field=models.ManyToManyField(blank=True, related_name='pedidos', to='caixa.carrinho'),
        ),
    ]
