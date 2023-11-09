# Converter o que está no Banco de Dados em JSON e vice-versa

from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email', 'cpf', 'nascimento',
        'telefone', 'rg', 'ruaResidencia', 'numeroResidencia', 
        'bairroResidencia','cepResidencia', 'estadoResidencia',
        'cidadeResidencia']