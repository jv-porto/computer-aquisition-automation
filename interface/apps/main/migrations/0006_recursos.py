# Generated by Django 4.0.4 on 2022-04-29 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_solicitacao_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recursos',
            fields=[
                ('semestre', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('valor_disponivel', models.IntegerField()),
                ('porcentagem_gp1', models.IntegerField()),
                ('porcentagem_gp2', models.IntegerField()),
                ('porcentagem_gp3', models.IntegerField()),
            ],
        ),
    ]
