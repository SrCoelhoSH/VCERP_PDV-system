# Generated by Django 4.1.13 on 2024-09-19 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcerp_caixa', '0003_alter_caixa_status_alter_caixa_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='caixa',
            name='data_abertura',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='caixa',
            name='data_fechamento',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
