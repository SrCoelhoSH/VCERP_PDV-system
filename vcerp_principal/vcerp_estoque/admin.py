from django.contrib import admin
from .models import PessoaFisica, PessoaJuridica, Produto, Profile
# Register your models here.

# Registre seus modelos aqui
admin.site.register(PessoaFisica)
admin.site.register(PessoaJuridica)
admin.site.register(Produto)
admin.site.register(Profile)



