# Generated by Django 4.1.13 on 2024-09-15 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcerp_estoque', '0010_produto_imagem_produto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
