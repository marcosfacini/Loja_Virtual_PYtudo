# Generated by Django 4.2 on 2023-07-06 03:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('produtos', '0025_alter_registroalteracaoproduto_produto'),
        ('vendas', '0003_itemvenda_venda_itemvenda_venda'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Carrinho',
            new_name='ListaDesejo',
        ),
    ]
