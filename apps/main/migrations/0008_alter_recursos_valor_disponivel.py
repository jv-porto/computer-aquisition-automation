# Generated by Django 4.0.4 on 2022-05-04 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_solicitacao_notebook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recursos',
            name='valor_disponivel',
            field=models.FloatField(),
        ),
    ]