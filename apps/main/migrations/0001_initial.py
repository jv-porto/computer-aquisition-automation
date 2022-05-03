# Generated by Django 4.0.4 on 2022-04-29 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estudante',
            fields=[
                ('matrícula', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
                ('idade', models.IntegerField()),
                ('renda', models.FloatField()),
                ('cor', models.CharField(choices=[('PRE', 'preta'), ('BRA', 'branca')], max_length=3)),
                ('sexo', models.CharField(choices=[('FEM', 'feminino'), ('MAS', 'masculino')], max_length=3)),
                ('ano_curso', models.FloatField()),
                ('escola', models.CharField(choices=[('PUB', 'pública'), ('PRI', 'privada')], max_length=3)),
                ('curso', models.IntegerField(choices=[(1, 'ciência de dados'), (2, 'direito'), (3, 'medicina'), (4, 'história'), (5, 'administração'), (6, 'engenharia biomédica'), (7, 'design'), (8, 'ciência da computação'), (9, 'filosofia')])),
                ('logradouro', models.CharField(max_length=200)),
                ('numero', models.IntegerField()),
                ('bairro', models.CharField(max_length=200)),
                ('cidade', models.CharField(max_length=200)),
                ('uf', models.CharField(max_length=2)),
                ('cep', models.CharField(max_length=9)),
                ('motivação', models.IntegerField()),
                ('porcentagem_concluida_curso', models.FloatField()),
                ('coordenadas_long_lat', models.CharField(max_length=200)),
                ('distrito', models.CharField(max_length=200)),
                ('distancia_ate_puc', models.FloatField()),
            ],
        ),
    ]
