# Converter o que está no Banco de Dados em JSON e vice-versa

from rest_framework import serializers
from core.models import *

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'password', 'last_login', 'is_superuser', 
                  'telefone', 'cpf', 'is_staff', 'created_at', 'is_active', 'email', 'objects']



class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['cliente', 'agencia', 'numero', 'digito', 'saldo', 'limite', 'chavePix']
        read_only_fields = ['id', 'cliente', 'agencia', 'numero', 'digito', 'saldo', 'limite']



class MovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = ('id','remetente','remetenteNome','destinatario','destinatarioNome','chavePix','tipo','valor','data','descricao',)



class CartoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartoes
        fields =('id', 'conta', 'tipo', 'numero', 'bandeira',)  

    