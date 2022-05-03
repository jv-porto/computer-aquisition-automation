from django.shortcuts import render, redirect

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



def sp_map():
    import geopandas as gpd

    sp_map = gpd.read_file('../../data/shapefiles/DEINFO_DISTRITO.shp')
    sp_map = sp_map.to_crs(4326)

    return sp_map



def geolocator():
    from configparser import ConfigParser
    from geopy.geocoders import GoogleV3

    config = ConfigParser()
    config.read('../../data/credentials.cfg')
    api_key= config.get('GOOGLE API', 'API_KEY')

    geolocator = GoogleV3(api_key=api_key)

    return geolocator



def geo_info(estudante):
    from shapely.geometry import Point
    import geopandas as gpd

    sp_map = sp_map()
    geolocator = geolocator()

    endereco = f'{estudante.logradouro}, {estudante.numero} - {estudante.bairro}, {estudante.cidade} - {estudante.uf}, Brasil, {estudante.cep}'
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



def analisar_solicitacoes(semestre_atual):
    recursos = Recursos.objects.get(pk=semestre_atual)
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





#################### POPULAR DATABASE COM DADOS JÁ MANIPULADOS ####################
def populate_db():
    import pandas as pd

    dados = pd.read_csv('assets/collectstatic/files/dados.csv')

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





#################### INDEX ####################
def index(request):
    return render(request, 'index/index.html')





#################### ESTUDANTES ####################
def estudantes(request):
    data = {'estudantes': Estudante.objects.all()}
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
            'idade': request.POST['idade'],
            'renda': request.POST['renda'],
            'cor': request.POST['cor'],
            'sexo': request.POST['sexo'],
            'ano_curso': request.POST['ano_curso'],
            'escola': request.POST['escola'],
            'curso': request.POST['curso'],
            'logradouro': request.POST['logradouro'],
            'numero': request.POST['numero'],
            'bairro': request.POST['bairro'],
            'cidade': request.POST['cidade'],
            'uf': request.POST['uf'],
            'cep': request.POST['cep'],
            'motivação': request.POST['motivação'],
        }
        
        coordenadas_long_lat, distrito, distancia_ate_puc = geo_info(estudante_infos)

        estudante_infos['porcentagem_concluida_curso'] = 100*(estudante_infos['ano_curso']/DURACAO_CURSOS[estudante_infos['curso']]),
        estudante_infos['coordenadas_long_lat'] = coordenadas_long_lat,
        estudante_infos['distrito'] = distrito,
        estudante_infos['distancia_ate_puc'] = distancia_ate_puc,
        
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
        estudante = Estudante.objects.get(pk=id)
        solicitacao = Solicitacao.objects.get(estudante=id)

        estudante_infos = {
            'nome': request.POST['nome'],
            'idade': request.POST['idade'],
            'renda': request.POST['renda'],
            'cor': request.POST['cor'],
            'sexo': request.POST['sexo'],
            'ano_curso': request.POST['ano_curso'],
            'escola': request.POST['escola'],
            'curso': request.POST['curso'],
            'logradouro': request.POST['logradouro'],
            'numero': request.POST['numero'],
            'bairro': request.POST['bairro'],
            'cidade': request.POST['cidade'],
            'uf': request.POST['uf'],
            'cep': request.POST['cep'],
            'motivação': request.POST['motivação'],
        }
        
        coordenadas_long_lat, distrito, distancia_ate_puc = geo_info(estudante_infos)

        estudante_infos['porcentagem_concluida_curso'] = 100*(estudante_infos['ano_curso']/DURACAO_CURSOS[estudante_infos['curso']]),
        estudante_infos['coordenadas_long_lat'] = coordenadas_long_lat,
        estudante_infos['distrito'] = distrito,
        estudante_infos['distancia_ate_puc'] = distancia_ate_puc,
        
        estudante.save()


        gp = grupo_prioritario(estudante_infos['renda'], estudante_infos['escola'], estudante_infos['cor'])
        
        solicitacao_infos = {
            'estudante': estudante,
            'notebook': Notebook.objects.get(pk=notebook(estudante_infos['curso'])),
            'grupo_prioritario': gp,
            'status': 'IND' if gp == 0 else 'ANA',
        }

        solicitacao.save()


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





#################### SOLICITAÇÕES ####################
def solicitacoes(request):
    if request.method == 'GET':
        return render(request, 'main/solicitacoes.html')
    elif request.method == 'POST':
        analisar_solicitacoes()
        return redirect('solicitacoes')





#################### NOTEBOOKS ####################
def notebooks(request):
    data = {'notebooks': Notebook.objects.all()}
    return render(request, 'main/notebooks.html', data)



def notebooks_incluir(request):
    if request.method == 'GET':
        return render(request, 'main/notebooks_incluir.html')
    elif request.method == 'POST':
        return redirect('notebooks')



def notebooks_alterar(request, id):
    if request.method == 'GET':
        data = {'notebooks': Notebook.objects.get(pk=id)}
        return render(request, 'main/notebooks_alterar.html', data)
    elif request.method == 'POST':
        return redirect('notebooks')



def notebooks_excluir(request, id):
    notebook = Notebook.objects.get(pk=id)
    notebook.delete()
    return redirect('notebooks')
