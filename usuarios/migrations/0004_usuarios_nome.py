# Generated by Django 4.1.3 on 2022-12-30 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_remove_usuarios_email_remove_usuarios_nome_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='nome',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]
