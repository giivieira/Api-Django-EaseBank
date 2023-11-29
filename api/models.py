from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager, 
    PermissionsMixin
)
from django.utils import timezone
from validate_docbr import CPF
from .sorteador import numeros, saldo, cartao


class UserManager(BaseUserManager):
    
    def criar_usuario(self, cpf, password=None, **extra_fields):
        if not cpf:
            raise ValueError("O usuário precisa inserir um CPF")

        cpf = ''.join(filter(str.isdigit, cpf))

        cpf_validator = CPF()
        if not cpf_validator.validate(cpf):
            raise ValueError("CPF inválido")

        cliente = self.model(cpf=cpf, **extra_fields)
        cliente.set_password(password)
        cliente.save()
        
        return cliente

    def create_superuser(self, cpf, password):
        
        cliente = self.criar_usuario(cpf, password)
        cliente.is_staff = True
        cliente.is_superuser = True
        cliente.save(using=self.db)
        
        return cliente
    
    
        
class Cliente(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=255, unique=False)
    last_name = models.CharField(max_length=255, unique=False)
    password = models.CharField(max_length=50)
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')
    is_superuser = models.BooleanField(default=False, verbose_name='superuser status')
    telefone = models.CharField(max_length=11, unique=False) 
    cpf = models.CharField(max_length=11, unique=True, null=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=255, unique=True)
    objects = UserManager() 
    USERNAME_FIELD = 'cpf'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'    
    


    
class Conta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agencia = models.IntegerField()
    numero = models.IntegerField()
    digito = models.IntegerField()
    saldo = models.DecimalField(max_digits=20, decimal_places=2)
    limite = models.DecimalField(max_digits=20, decimal_places=2)
    chavePix = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.cliente.nome
    


    
class Cartoes(models.Model):
    DEBITO = 'd'
    CREDITO = 'c'
    CREBITO = 'b'
    CARTOESLISTA = (
        (DEBITO, "Debito"),
        (CREDITO, "Credito"),
        (CREBITO, "Crebito")
    )
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=CARTOESLISTA, default=CREBITO)
    numero= models.CharField(max_length=20, default="", unique=True)
    bandeira = models.CharField(max_length=1, default='G')



    
class Movimentacao(models.Model):
    PIX = 'p'
    TRANSFERENCIA = 't'
    DEPOSITO = 'd'
    TIPOS = (
        (PIX, "PIX"),
        (TRANSFERENCIA, "Transferência"),
        (DEPOSITO, "Depósito")
    )
    remetente = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name="remetente")
    remetenteNome = models.CharField(max_length=100)
    destinatario = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name="destinatario")
    destinatarioNome = models.CharField(max_length=100)
    chavePix = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=TIPOS) # PIX TRANFERENCIA PAGAMENTO
    valor = models.DecimalField(max_digits=10, decimal_places=2, default="p")
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=100)
