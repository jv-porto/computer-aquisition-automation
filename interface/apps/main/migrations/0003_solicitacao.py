# Generated by Django 4.0.4 on 2022-04-29 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_notebook'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitacao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('DEF', 'deferida'), ('IND', 'indeferida')], max_length=3)),
                ('estudante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.estudante')),
            ],
        ),
    ]
