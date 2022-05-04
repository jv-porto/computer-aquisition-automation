# Generated by Django 4.0.4 on 2022-04-29 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_solicitacao_grupo_prioritario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacao',
            name='status',
            field=models.CharField(choices=[('DEF', 'deferida'), ('IND', 'indeferida'), ('ANA', 'em análise')], max_length=3),
        ),
    ]