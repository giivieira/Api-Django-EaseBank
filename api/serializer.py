# Converter o que está no Banco de Dados em JSON e vice-versa

from rest_framework import serializers
from api.models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['first_name','last_name', 'password', 'last_login', 'is_superuser', 
                  'telefone', 'cpf', 'is_staff', 'created_at', 'is_active', 'email', 'objects']

