from django.contrib import admin

from .models import Estudante, Notebook, Solicitacao

admin.site.register(Estudante)
admin.site.register(Notebook)
admin.site.register(Solicitacao)
