from unittest import result
from django.shortcuts import render, redirect
from django.core.exceptions import BadRequest

from .models import Estudante, Notebook, Solicitacao, Recursos





#################### VARIÁVEIS E FUNÇÕES COMUNS ####################
SALARIO_MINIMO = 1212
DURACAO_CURSOS = {
    1: 3.5,  # ciência de dados
    2: 5,  # direito
    3: 6,  # medicina
    4: 4,  # história
    5: 4,  # administração
    6: 5,  # engenharia biomédica
    7: 3,  # design
    8: 4,  # ciência da computação
    9: 3,  # filosofia
}
PUC_COORDS = (-46.671184851274276, -23.53807279812106)


class ResultadosFinais():
    def deferidas(grupo):
        q_count = Solicitacao.objects.filter(grupo_prioritario=grupo, status='DEF').count()
        return q_count

    def indeferidas(grupo):
        q_count = Solicitacao.objects.filter(grupo_prioritario=grupo, status='IND').count()
        return q_count

    def total(grupo):
        q_count = Solicitacao.objects.filter(grupo_prioritario=grupo).count()
        return q_count



def get_sp_map():
    import geopandas as gpd

    sp_map = gpd.read_file('assets/collectstatic/files/data/shapefiles/DEINFO_DISTRITO.shp')
    sp_map = sp_map.to_crs(4326)

    return sp_map



def get_geolocator():
    import os
    from geopy.geocoders import GoogleV3

    api_key = os.environ.get('GOOGLE_API_KEY')

    geolocator = GoogleV3(api_key=api_key)

    return geolocator



def geo_info(estudante):
    from shapely.geometry import Point
    import geopandas as gpd

    sp_map = get_sp_map()
    geolocator = get_geolocator()

    endereco = f"{estudante['logradouro']}, {estudante['numero']} - {estudante['bairro']}, {estudante['cidade']} - {estudante['uf']}, Brasil, {estudante['cep']}"
    location = geolocator.geocode(endereco)

    coordenadas_long_lat = f'{location.longitude}, {location.latitude}'

    mapa_distancia = gpd.GeoDataFrame({'geometry': [Point(PUC_COORDS), Point(eval(coordenadas_long_lat))]}, crs='EPSG:4326')
    mapa_distancia = mapa_distancia.to_crs('EPSG:5880')
    distancia_ate_puc = mapa_distancia.distance(mapa_distancia.shift())[1]
    
    try:
        distrito = sp_map[sp_map.contains(Point(eval(coordenadas_long_lat))) == True].NOME_DIST.iloc[0]
    except:
        distrito = sp_map.loc[sp_map.distance(Point(eval(coordenadas_long_lat))).sort_values().index[0], 'NOME_DIST']

    return coordenadas_long_lat, distrito, distancia_ate_puc



def grupo_prioritario(renda, escola, cor):
            if renda > 3*SALARIO_MINIMO:
                return 0
            elif escola == 'PUB':
                return 1
            elif cor == 'PRE':
                return 2
            else:
                return 3



def notebook(curso):
    computador_por_curso = {
        1: 1,  # ciência de dados
        2: 3,  # direito
        3: 3,  # medicina
        4: 3,  # história
        5: 2,  # administração
        6: 2,  # engenharia biomédica
        7: 1,  # design
        8: 1,  # ciência da computação
        9: 3,  # filosofia
    }

    return computador_por_curso[curso]





#################### INDEX ####################
def index(request):
    return render(request, 'index/index.html')





#################### ESTUDANTES ####################
def estudantes(request):
    data = {'estudantes': Estudante.objects.all().order_by('matrícula')}
    return render(request, 'main/estudantes.html', data)



def estudantes_info(request, id):
    data = {'estudante': Estudante.objects.get(pk=id)}
    return render(request, 'main/estudantes_info.html', data)



def estudantes_incluir(request):
    if request.method == 'GET':
        return render(request, 'main/estudantes_incluir.html')
    elif request.method == 'POST':
        estudante_infos = {
            'matrícula': request.POST['matrícula'],
            'nome': request.POST['nome'],
            'idade': int(request.POST['idade']),
            'renda': float(request.POST['renda'].replace('.', '').replace(',', '.')),
            'cor': request.POST['cor'],
            'sexo': request.POST['sexo'],
            'ano_curso': float(request.POST['ano_curso'].replace(',', '.')),
            'escola': request.POST['escola'],
            'curso': int(request.POST['curso']),
            'logradouro': request.POST['logradouro'],
            'numero': int(request.POST['numero']),
            'bairro': request.POST['bairro'],
            'cidade': request.POST['cidade'],
            'uf': request.POST['uf'],
            'cep': request.POST['cep'],
            'motivação': int(request.POST['motivação']),
        }
        
        coordenadas_long_lat, distrito, distancia_ate_puc = geo_info(estudante_infos)

        estudante_infos['porcentagem_concluida_curso'] = 100*(estudante_infos['ano_curso']/DURACAO_CURSOS[estudante_infos['curso']])
        estudante_infos['coordenadas_long_lat'] = coordenadas_long_lat
        estudante_infos['distrito'] = distrito
        estudante_infos['distancia_ate_puc'] = distancia_ate_puc
        
        estudante = Estudante.objects.create(**estudante_infos)
        estudante.save()


        gp = grupo_prioritario(estudante_infos['renda'], estudante_infos['escola'], estudante_infos['cor'])
        
        solicitacao_infos = {
            'estudante': estudante,
            'notebook': Notebook.objects.get(pk=notebook(estudante_infos['curso'])),
            'grupo_prioritario': gp,
            'status': 'IND' if gp == 0 else 'ANA',
        }

        solicitacao = Solicitacao.objects.create(**solicitacao_infos)
        solicitacao.save()


        return redirect('estudantes')



def estudantes_alterar(request, id):
    if request.method == 'GET':
        data = {'estudante': Estudante.objects.get(pk=id)}
        return render(request, 'main/estudantes_alterar.html', data)
    elif request.method == 'POST':
        estudante_infos = {
            'nome': request.POST['nome'],
            'idade': int(request.POST['idade']),
            'renda': float(request.POST['renda'].replace('.', '').replace(',', '.')),
            'cor': request.POST['cor'],
            'sexo': request.POST['sexo'],
            'ano_curso': float(request.POST['ano_curso'].replace(',', '.')),
            'escola': request.POST['escola'],
            'curso': int(request.POST['curso']),
            'logradouro': request.POST['logradouro'],
            'numero': int(request.POST['numero']),
            'bairro': request.POST['bairro'],
            'cidade': request.POST['cidade'],
            'uf': request.POST['uf'],
            'cep': request.POST['cep'],
            'motivação': int(request.POST['motivação']),
        }
        
        coordenadas_long_lat, distrito, distancia_ate_puc = geo_info(estudante_infos)

        estudante_infos['porcentagem_concluida_curso'] = 100*(estudante_infos['ano_curso']/DURACAO_CURSOS[estudante_infos['curso']])
        estudante_infos['coordenadas_long_lat'] = coordenadas_long_lat
        estudante_infos['distrito'] = distrito
        estudante_infos['distancia_ate_puc'] = distancia_ate_puc
        
        Estudante.objects.update_or_create(pk=id, defaults=estudante_infos)


        gp = grupo_prioritario(estudante_infos['renda'], estudante_infos['escola'], estudante_infos['cor'])
        
        solicitacao_infos = {
            'estudante': Estudante.objects.get(pk=id),
            'notebook': Notebook.objects.get(pk=notebook(estudante_infos['curso'])),
            'grupo_prioritario': gp,
            'status': 'IND' if gp == 0 else 'ANA',
        }

        Solicitacao.objects.update_or_create(estudante=id, defaults=solicitacao_infos)


        return redirect('estudantes_info', id)



def estudantes_excluir(request, id):
    solicitacao_estudante = Solicitacao.objects.get(estudante=id)
    solicitacao_estudante.delete()

    estudante = Estudante.objects.get(pk=id)
    estudante.delete()

    return redirect('estudantes')



def estudantes_status(request, id):
    data = {'estudante': Estudante.objects.get(pk=id), 'solicitacao': Solicitacao.objects.get(estudante=id)}
    return render(request, 'main/estudantes_status.html', data)





#################### RECURSOS E SOLICITAÇÕES ####################
def recursos(request):
    data = {'recursos': Recursos.objects.all().order_by('semestre')}
    return render(request, 'main/recursos.html', data)



def recursos_info(request, semestre):
    resultados_finais = {
        'deferidas_gp1': ResultadosFinais.deferidas(grupo=1),
        'indeferidas_gp1': ResultadosFinais.indeferidas(grupo=1),
        'total_gp1': ResultadosFinais.total(grupo=1),

        'deferidas_gp2': ResultadosFinais.deferidas(grupo=2),
        'indeferidas_gp2': ResultadosFinais.indeferidas(grupo=2),
        'total_gp2': ResultadosFinais.total(grupo=2),
        
        'deferidas_gp3': ResultadosFinais.deferidas(grupo=3),
        'indeferidas_gp3': ResultadosFinais.indeferidas(grupo=3),
        'total_gp3': ResultadosFinais.total(grupo=3),
    }

    data = {'recurso': Recursos.objects.get(pk=semestre), 'em_analise': Solicitacao.objects.filter(status='ANA').exists(), 'resultados_finais': resultados_finais}
    return render(request, 'main/recursos_info.html', data)



def recursos_incluir(request):
    if request.method == 'GET':
        return render(request, 'main/recursos_incluir.html')
    elif request.method == 'POST':
        recursos_infos = {
            'semestre': request.POST['semestre'].replace('/', '_'),
            'valor_disponivel': float(request.POST['valor_disponivel'].replace('.', '').replace(',', '.')),
            'porcentagem_gp1': float(request.POST['porcentagem_gp1'].replace(',', '.')),
            'porcentagem_gp2': float(request.POST['porcentagem_gp2'].replace(',', '.')),
            'porcentagem_gp3': float(request.POST['porcentagem_gp3'].replace(',', '.')),
        }

        recursos = Recursos.objects.create(**recursos_infos)
        recursos.save()

        return redirect('recursos')



def recursos_alterar(request, semestre):
    if request.method == 'GET':
        data = {'recurso': Recursos.objects.get(pk=semestre)}
        return render(request, 'main/recursos_alterar.html', data)
    elif request.method == 'POST':
        recursos_infos = {
            'valor_disponivel': float(request.POST['valor_disponivel'].replace('.', '').replace(',', '.')),
            'porcentagem_gp1': float(request.POST['porcentagem_gp1'].replace(',', '.')),
            'porcentagem_gp2': float(request.POST['porcentagem_gp2'].replace(',', '.')),
            'porcentagem_gp3': float(request.POST['porcentagem_gp3'].replace(',', '.')),
        }

        Recursos.objects.update_or_create(pk=semestre, defaults=recursos_infos)
        
        return redirect('recursos_info', semestre)



def recursos_excluir(request, semestre):
    recursos = Recursos.objects.get(pk=semestre)
    recursos.delete()

    return redirect('recursos')



def solicitacoes_analisar(request, semestre):
    recursos = Recursos.objects.get(pk=semestre)
    valor_disponivel_por_gp = {
        1: recursos.valor_disponivel*(recursos.porcentagem_gp1/100),
        2: recursos.valor_disponivel*(recursos.porcentagem_gp2/100),
        3: recursos.valor_disponivel*(recursos.porcentagem_gp3/100),
    }


    def analisar_gp(q, valor, status_negativo):
        for i in range(len(q)):
            if valor >= q[i].notebook.preco:
                valor -= q[i].notebook.preco

                q[i].status = 'DEF'
                q[i].save()
            else:
                q[i].status = status_negativo
                q[i].save()

        return valor

    valor_restante = 0
    for gp, valor_disponivel in valor_disponivel_por_gp.items():
        q = Solicitacao.objects.filter(grupo_prioritario=gp).order_by('estudante__renda', 'estudante__idade')
        valor_restante += analisar_gp(q, valor_disponivel, 'ANA')
    
    for gp in valor_disponivel_por_gp.keys():
        q = Solicitacao.objects.filter(grupo_prioritario=gp, status='ANA').order_by('estudante__renda', 'estudante__idade')
        valor_restante = analisar_gp(q, valor_restante, 'IND')

    return redirect('recursos')





#################### NOTEBOOKS ####################
def notebooks(request):
    data = {'notebooks': Notebook.objects.all().order_by('id')}
    return render(request, 'main/notebooks.html', data)



def notebooks_info(request, id):
    data = {'notebook': Notebook.objects.get(pk=id)}
    return render(request, 'main/notebooks_info.html', data)



def notebooks_incluir(request):
    if request.method == 'GET':
        return render(request, 'main/notebooks_incluir.html')
    elif request.method == 'POST':
        notebook_infos = {
            'id': request.POST['id_notebook'],
            'marca': request.POST['marca'],
            'modelo': request.POST['modelo'],
            'especificacoes_tecnicas': request.POST['especificacoes_tecnicas'],
            'preco': float(request.POST['preco'].replace('.', '').replace(',', '.')),
        }

        notebook = Notebook.objects.create(**notebook_infos)
        notebook.save()

        return redirect('notebooks')



def notebooks_alterar(request, id):
    if request.method == 'GET':
        data = {'notebook': Notebook.objects.get(pk=id)}
        return render(request, 'main/notebooks_alterar.html', data)
    elif request.method == 'POST':
        notebook_infos = {
            'marca': request.POST['marca'],
            'modelo': request.POST['modelo'],
            'especificacoes_tecnicas': request.POST['especificacoes_tecnicas'],
            'preco': float(request.POST['preco'].replace('.', '').replace(',', '.')),
        }

        Notebook.objects.update_or_create(pk=id, defaults=notebook_infos)

        return redirect('notebooks_info', id)



def notebooks_excluir(request, id):
    notebook = Notebook.objects.get(pk=id)
    notebook.delete()
    return redirect('notebooks')





#################### POPULAR BASE DE DADOS COM O DATASET FORNECIDO ####################
def populate_db(request):
    import pandas as pd

    dados = pd.read_csv('assets/collectstatic/files/data/dados.csv')

    choices = {
        'cor': {
            'preta': 'PRE',
            'branca': 'BRA',
        },
        'sexo': {
            'feminino': 'FEM',
            'masculino': 'MAS',
        },
        'escola': {
            'pública': 'PUB',
            'privada': 'PRI',
        },
        'curso': {
            'ciência de dados': 1,
            'direito': 2,
            'medicina': 3,
            'história': 4,
            'administração': 5,
            'engenharia biomédica': 6,
            'design': 7,
            'ciência da computação': 8,
            'filosofia': 9,
        }
    }

    for index, row in dados.iterrows():
        estudante_infos = {
            'matrícula': row['matrícula'],
            'nome': row['nome'],
            'idade': row['idade'],
            'renda': row['renda'],
            'cor': choices['cor'][row['cor']],
            'sexo': choices['sexo'][row['sexo']],
            'ano_curso': row['ano_curso'],
            'escola': choices['escola'][row['escola']],
            'curso': choices['curso'][row['curso']],
            'logradouro': row['logradouro'],
            'numero': row['numero'],
            'bairro': row['bairro'],
            'cidade': row['cidade'],
            'uf': row['uf'],
            'cep': row['cep'],
            'motivação': row['motivação'],
            'porcentagem_concluida_curso': row['porcentagem_concluida_curso'],
            'coordenadas_long_lat': row['coordenadas_long_lat'],
            'distrito': row['distrito'],
            'distancia_ate_puc': row['distancia_ate_puc'],
        }
        estudante = Estudante.objects.create(**estudante_infos)
        estudante.save()

        gp = grupo_prioritario(estudante_infos['renda'], estudante_infos['escola'], estudante_infos['cor'])
        solicitacao_infos = {
            'estudante': estudante,
            'notebook': Notebook.objects.get(pk=notebook(estudante_infos['curso'])),
            'grupo_prioritario': gp,
            'status': 'IND' if gp == 0 else 'ANA',
        }
        solicitacao = Solicitacao.objects.create(**solicitacao_infos)
        solicitacao.save()


        return redirect('index')
