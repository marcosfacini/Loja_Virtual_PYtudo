# Generated by Django 4.2 on 2023-05-16 15:58

import cpf_field.models
from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_usuarios_cpf_alter_usuarios_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='celular',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='cpf',
            field=cpf_field.models.CPFField(max_length=14, verbose_name='CPF'),
        ),
    ]
