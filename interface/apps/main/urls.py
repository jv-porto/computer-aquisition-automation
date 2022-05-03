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

    path('solicitacoes/', solicitacoes, name='solicitacoes'),

    path('notebooks/', notebooks, name='notebooks'),
    path('notebooks/incluir/', notebooks_incluir, name='notebooks_incluir'),
    path('notebooks/alterar/<str:id>/', notebooks_alterar, name='notebooks_alterar'),
    path('notebooks/excluir/<str:id>/', notebooks_excluir, name='notebooks_excluir'),
]
