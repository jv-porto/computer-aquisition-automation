from django.db import models


class Estudante(models.Model):
    cor_choices = [
        ('PRE', 'preta'),
        ('BRA', 'branca'),
    ]
    sexo_choices = [
        ('FEM', 'feminino'),
        ('MAS', 'masculino'),
    ]
    escola_choices = [
        ('PUB', 'pública'),
        ('PRI', 'privada'),
    ]
    curso_choices = [
        (1, 'ciência de dados'),
        (2, 'direito'),
        (3, 'medicina'),
        (4, 'história'),
        (5, 'administração'),
        (6, 'engenharia biomédica'),
        (7, 'design'),
        (8, 'ciência da computação'),
        (9, 'filosofia'),
    ]

    matrícula = models.CharField(primary_key=True, max_length=10)
    nome = models.CharField(max_length=200)
    idade = models.IntegerField()
    renda = models.FloatField()
    cor = models.CharField(max_length=3, choices=cor_choices)
    sexo = models.CharField(max_length=3, choices=sexo_choices)
    ano_curso = models.FloatField()
    escola = models.CharField(max_length=3, choices=escola_choices)
    curso = models.IntegerField(choices=curso_choices)
    logradouro = models.CharField(max_length=200)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    motivação = models.IntegerField()
    porcentagem_concluida_curso = models.FloatField()
    coordenadas_long_lat = models.CharField(max_length=200)
    distrito = models.CharField(max_length=200)
    distancia_ate_puc = models.FloatField()


class Notebook(models.Model):
    id = models.IntegerField(primary_key=True)
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    especificacoes_tecnicas = models.TextField()
    preco = models.FloatField()


class Solicitacao(models.Model):
    status_choices = [
        ('DEF', 'deferida'),
        ('IND', 'indeferida'),
        ('ANA', 'em análise'),
    ]
    gp_choices = [
        (1, 'Oriundos de escola pública'),
        (2, 'Pretos oriundos de escola privada'),
        (3, 'Brancos oriundos de escola privada'),
        (0, 'Não possui'),
    ]

    id = models.AutoField(primary_key=True)
    estudante = models.ForeignKey('Estudante', on_delete=models.CASCADE)
    notebook = models.ForeignKey('Notebook', on_delete=models.CASCADE)
    grupo_prioritario = models.CharField(max_length=1, choices=gp_choices)
    status = models.CharField(max_length=3, choices=status_choices)


class Recursos(models.Model):
    semestre = models.CharField(max_length=6, primary_key=True)
    valor_disponivel = models.FloatField()
    porcentagem_gp1 = models.FloatField()
    porcentagem_gp2 = models.FloatField()
    porcentagem_gp3 = models.FloatField()
