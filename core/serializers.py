from rest_framework import serializers
from models import *

class MovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = ('id','remetente','remetenteNome','destinatario','destinatarioNome','chavePix','tipo','valor','data','descricao',)