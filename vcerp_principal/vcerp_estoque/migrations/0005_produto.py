# Generated by Django 4.1.13 on 2024-09-03 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcerp_estoque', '0004_pessoafisica_penalizado_pessoajuridica_penalizado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('eletronico', 'Eletrônico'), ('vestuario', 'Vestuário'), ('alimento', 'Alimento')], max_length=20)),
                ('descricao', models.TextField()),
                ('codigo_barra', models.CharField(max_length=50)),
                ('data_cadastro', models.DateField()),
                ('quantidade', models.PositiveIntegerField()),
            ],
        ),
    ]
