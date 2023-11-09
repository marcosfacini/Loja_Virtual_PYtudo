# Generated by Django 4.2 on 2023-11-09 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='banners/')),
                ('home', models.BooleanField(default=False)),
                ('titulo', models.CharField(blank=True, max_length=50, null=True)),
                ('subtitulo', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
