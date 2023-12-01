from django.shortcuts import render
from rest_framework import viewsets
from models import *
from rest_framework import serializers
from rest_framework_simplejwt import authentication as authenticationJWT
from user.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action

class MovimentacaoViewSet(viewsets.ViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = serializers.MovimentacaoSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], )
    def lista_transferencia(self, request):
        auth_user = request.user

        if auth_user:
            conta = Conta.objects.filter(user=auth_user).first()

            if conta:
                transacoes_conta = Movimentacao.objects.filter(Q(conta_origem=conta) | Q(conta_destino=conta)).order_by('-id')
                extrato = []

                saldo_atual = conta.saldo
                
                
                ##### TERMINAR DAQUI PARA BAIXO #######

                for movimentacao in movimentacoes_conta: #########
                    extrato.append({
                        'created_at': transacao.created_at,
                        'valor': transacao.valor,
                        'descricao': transacao.descricao,
                        'saldo_atual': saldo_atual
                    })

                    if transacao.conta_origem.id == conta.id:
                        saldo_atual -= transacao.valor
                    elif transacao.conta_destino.id == conta.id:
                        saldo_atual += transacao.valor

                return Response(extrato, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Conta não encontrada para o usuário logado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(detail=False, methods=['post'])
    def transferencia(self, request):
        serializer = serializers.TransacaoSerializer(data=request.data)
        auth_user = request.user

        if serializer.is_valid():
            conta_destino_id = serializer.validated_data.get('conta_origem')
            valor = serializer.validated_data.get('valor')
            descricao = serializer.validated_data.get('descricao')
            cartao = serializer.validated_data.get('cartao')

            conta_origem = Conta.objects.filter(user=auth_user).first()
            print("Conta origem: ", conta_origem)
            conta_destino = Conta.objects.filter(id=conta_destino_id).first()
            print("Conta destino: ", conta_destino)
            if conta_origem and conta_destino:
                if conta_origem.saldo >= valor:
                    transacao = Transacao.objects.create(
                        conta_destino=conta_destino,
                        conta_origem=conta_origem,
                        valor=valor,
                        descricao=descricao,
                        cartao_id=cartao.id 
                    )

                    conta_origem.saldo -= valor
                    conta_destino.saldo += valor

                    conta_origem.save()
                    conta_destino.save()

                    return Response({"message": "Transação realizada com sucesso"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "Saldo insuficiente na conta de origem"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Conta de origem ou destino não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ⣿⣿