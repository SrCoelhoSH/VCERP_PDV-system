# Generated by Django 4.1.13 on 2024-09-14 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcerp_estoque', '0009_transacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='imagem_produto',
            field=models.ImageField(blank=True, null=True, upload_to='produtos/'),
        ),
    ]
