# Generated by Django 4.2 on 2023-07-06 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0025_alter_registroalteracaoproduto_produto'),
        ('vendas', '0005_alter_listadesejo_produtos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listadesejo',
            name='produtos',
            field=models.ManyToManyField(blank=True, related_name='produtos', to='produtos.produtos'),
        ),
    ]
