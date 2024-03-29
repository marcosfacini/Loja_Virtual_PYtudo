# Generated by Django 4.2 on 2023-12-15 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_remove_pedido_informacoes_adicionais_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('WAITING', 'WAITING'), ('AUTHORIZED', 'AUTHORIZED'), ('IN_ANALYSIS', 'IN_ANALYSIS'), ('DECLINED', 'DECLINED'), ('PAID', 'PAID'), ('CANCELED', 'CANCELED')], default='WAITING', max_length=100),
        ),
    ]
