# Generated by Django 4.2 on 2023-04-20 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0002_alter_produtos_preco'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtos',
            name='quantidade',
            field=models.IntegerField(default=0),
        ),
    ]