from django.urls import path

from .views import *


urlpatterns = [
    path('', index, name='index'),

    path('estudantes/', estudantes, name='estudantes'),
    path('estudantes/incluir/', estudantes_incluir, name='estudantes_incluir'),
    path('estudantes/<str:id>/', estudantes_info, name='estudantes_info'),
    path('estudantes/<str:id>/alterar/', estudantes_alterar, name='estudantes_alterar'),
    path('estudantes/<str:id>/excluir/', estudantes_excluir, name='estudantes_excluir'),
    path('estudantes/<str:id>/status/', estudantes_status, name='estudantes_status'),

    path('recursos/', recursos, name= 'recursos'),
    path('recursos/incluir/', recursos_incluir, name= 'recursos_incluir'),
    path('recursos/<str:semestre>/', recursos_info, name= 'recursos_info'),
    path('recursos/<str:semestre>/alterar/', recursos_alterar, name= 'recursos_alterar'),
    path('recursos/<str:semestre>/excluir/', recursos_excluir, name= 'recursos_excluir'),
    path('solicitacoes/<str:semestre>/analisar/', solicitacoes_analisar, name='solicitacoes_analisar'),

    path('notebooks/', notebooks, name='notebooks'),
    path('notebooks/incluir/', notebooks_incluir, name='notebooks_incluir'),
    path('notebooks/<str:id>/', notebooks_info, name='notebooks_info'),
    path('notebooks/<str:id>/alterar/', notebooks_alterar, name='notebooks_alterar'),
    path('notebooks/<str:id>/excluir/', notebooks_excluir, name='notebooks_excluir'),
    
    path('db/resetar/', resetar_db, name='resetar_db'),
    path('db/popular/', popular_db, name='popular_db'),
]
