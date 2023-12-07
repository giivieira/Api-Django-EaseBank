from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.http import HttpResponseBadRequest
from rest_framework_simplejwt.tokens import AccessToken
import decimal
from django.db.models import Q
from rest_framework_simplejwt import authentication as authenticationJWT
import random
from rest_framework.decorators import action
from api.serializer import MovimentacaoSerializer

# @api_view(['GET', 'POST'])
# def listar_clientes(request):
#     if request.method == 'GET':
#         queryset = Cliente.objects.all()
#         serializer = ClienteSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ClienteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'POST'])
def exibir_conta(request):
    if request.method == 'GET':
        queryset = Conta.objects.all()
        serializer = ContaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_id(request):
    token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
    print(token)
    remetente = AccessToken(token)
    contaRemetenteId = remetente['user_id']
    return contaRemetenteId

# class ClientesView(ListCreateAPIView):
#     queryset = Cliente.objects.all()
#     serializer_class = ClienteSerializer

# class ClientesDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Cliente.objects.all()
#     serializer_class = ClienteSerializer
        
class ContaView(viewsets.ModelViewSet):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            agencia = '0001'
            numero = ''
            for n in range(8):
                numero += str(random.randint(0, 9))

            conta = Conta(
                cliente=self.request.user,
                numero=numero,
                agencia=agencia,
                saldo=1000,
                chavePix=serializer.validated_data.get("chavePix"),
                limite=1000,
                digito=1
            )

            conta.save()

            return Response({"message": "created"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class CartaoView(generics.ListCreateAPIView):
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Cartoes.objects.all()
    serializer_class = CartoesSerializer


class CartoesListarDetalhar(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Cartoes.objects.all()
    serializer_class = CartoesSerializer
    
    def create(self, request, *args, **kwargs):
        id = get_id(request)
        conta = Conta.objects.get(cliente=id)
        print(conta)
        tipo = request.data['tipo']        

        if tipo == 'd' and Cartoes.objects.filter(conta=conta, tipo='d').exists():
            return HttpResponseBadRequest("Já existe um cartão do tipo 'débito' associado a esta conta.")
        
        if tipo == 'c' and Cartoes.objects.filter(conta=conta, tipo='c').count() >= 5:
            return HttpResponseBadRequest("Limite máximo de cartões do tipo 'crédito' atingido para esta conta.")
        
        numero = cartao()
        resposta = Cartoes.objects.create(conta=conta, tipo=tipo, numero=numero)
        
        return Response(CartoesSerializer(resposta).data,200)


class MovimentacaoListarDetalhar(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer

    def create(self, request, *args, **kwargs):
        contaRemetenteId = get_id(request)
        conta_remetente = Conta.objects.get(cliente=int(contaRemetenteId))

        print(request.data)
        
        # #pegar o token e obter o user_id
        # print("dest :",destinatario)
        conta_destinatario = Conta.objects.get(chavePix=request.data['chavePix'])
        destinatario = conta_destinatario.cliente

        if conta_destinatario is None:
            raise serializers.ValidationError('destinatario nao existe')
        if conta_remetente is None:
            raise serializers.ValidationError('remetente nao existe')
        if conta_remetente.saldo <= decimal.Decimal(request.data['valor']):
            print("teste")
            raise serializers.ValidationError('Saldo is not suficiente')
        
        if contaRemetenteId == conta_destinatario.id:
            raise serializers.ValidationError('conta e destinatario sao os mesmos')
        
        conta_remetente.saldo -= decimal.Decimal(request.data['valor'])
        conta_remetente.save()
        
        conta_destinatario.saldo += decimal.Decimal(request.data['valor'])
        conta_destinatario.save()

        _mutable = request.data._mutable

        # set to mutable
        request.data._mutable = True
        request.data['remetente'] = contaRemetenteId
        request.data['remetenteNome'] = conta_remetente.cliente.first_name
        request.data['destinatario'] = conta_destinatario.id
        request.data['destinatarioNome'] = destinatario.first_name
        request.data._mutable = False
        request.data._mutable = _mutable

        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        id_user = get_id(request)
        Conta.objects.get(id=id_user)
        movimentacoes = Movimentacao.objects.filter(Q(remetente=id_user) | Q(destinatario=id_user)).order_by("-data")
        
        return Response(MovimentacaoSerializer(movimentacoes, many=True).data)
    
class MovimentacaoViewSet(viewsets.ViewSet):
    queryset = Movimentacao.objects.all()
    serializer_class = MovimentacaoSerializer
    authentication_classes = [authenticationJWT.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path="listar")
    def lista_transferencia(self, request):
        auth_user = request.user
        print(auth_user)

        if auth_user:
            conta = Conta.objects.filter(cliente=auth_user).first()

            if conta:
                transacoes_conta = Movimentacao.objects.filter(Q(remetente=conta) | Q(destinatario=conta)).order_by('-id')
                extrato = []

                saldo_atual = conta.saldo

                for movimentacao in transacoes_conta: #########
                    extrato.append({
                        'created_at': movimentacao.created_at,
                        'valor': movimentacao.valor,
                        'descricao': movimentacao.descricao,
                        'saldo_atual': saldo_atual
                    })

                    if movimentacao.conta_origem.id == conta.id:
                        saldo_atual -= movimentacao.valor
                    elif movimentacao.conta_destino.id == conta.id:
                        saldo_atual += movimentacao.valor

                return Response(extrato, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Conta não encontrada para o usuário logado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Usuário não autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(detail=False, methods=['post'], url_path="fazer")
    def transferencia(self, request):
        serializer = MovimentacaoSerializer(data=request.data)
        auth_user = request.user

        if serializer.is_valid():
            destinatario = serializer.validated_data.get('destinatario')
            destinatarioNome = serializer.validated_data.get('destinatarioNome')
            remetente = serializer.validated_data.get('remetente')
            remetenteNome = serializer.validated_data.get('remetenteNome')
            valor = serializer.validated_data.get('valor')
            descricao = serializer.validated_data.get('descricao')
            cartao = serializer.validated_data.get('cartao')
            chavePix = serializer.validated_data.get('chavePix')
            data = serializer.validated_data.get('data')
            


            remetente = Conta.objects.filter(cliente=auth_user).first()
            print("Conta origem: ", remetente)
            conta_destino = Conta.objects.filter(id=destinatario.id).first()
            print("Conta destino: ", conta_destino)
            if remetente and conta_destino:
                if remetente.saldo >= decimal.Decimal(valor):
                    movimentacao = Movimentacao.objects.create(
                        destinatario=destinatario,
                        destinatarioNome=destinatarioNome,
                        remetente=remetente,
                        remetenteNome=remetenteNome,
                        valor=valor,
                        descricao=descricao,
                        chavePix=chavePix,
                        data = data,
                        # cartao_id=cartao.id 
                    )

                    remetente.saldo -= valor
                    destinatario.saldo += valor

                    remetente.save()
                    destinatario.save()

                    return Response({"message": "Transação realizada com sucesso"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "Saldo insuficiente na conta de origem"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Conta de origem ou destino não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



