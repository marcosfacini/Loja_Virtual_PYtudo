# Generated by Django 4.2 on 2023-04-27 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0006_marca_alter_produtos_categoria_produtos_marca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='marca',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produtos',
            name='quantidade',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='Marca',
        ),
    ]