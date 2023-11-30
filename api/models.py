from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager, 
    PermissionsMixin
)
from django.utils import timezone
from validate_docbr import CPF
from .sorteador import numeros, saldo, cartao


# class UserManager(BaseUserManager):
    
#     def criar_usuario(self, cpf, password=None, **extra_fields):
#         if not cpf:
#             raise ValueError("O usuário precisa inserir um CPF")

#         cpf = ''.join(filter(str.isdigit, cpf))

#         cpf_validator = CPF()
#         if not cpf_validator.validate(cpf):
#             raise ValueError("CPF inválido")

#         cliente = self.model(cpf=cpf, **extra_fields)
#         cliente.set_password(password)
#         cliente.save()
        
#         return cliente

#     def create_superuser(self, cpf, password):
        
#         cliente = self.criar_usuario(cpf, password)
#         cliente.is_staff = True
#         cliente.is_superuser = True
#         cliente.save(using=self.db)
        
#         return cliente
    
    
        
# class Cliente(AbstractBaseUser, PermissionsMixin):

#     first_name = models.CharField(max_length=255, unique=False)
#     last_name = models.CharField(max_length=255, unique=False)
#     password = models.CharField(max_length=50)
#     last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')
#     is_superuser = models.BooleanField(default=False, verbose_name='superuser status')
#     telefone = models.CharField(max_length=11, unique=False) 
#     cpf = models.CharField(max_length=11, unique=True, null=False)
#     is_staff = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=timezone.now)
#     is_active = models.BooleanField(default=True)
#     email = models.EmailField(max_length=255, unique=True)
#     objects = UserManager() 
#     USERNAME_FIELD = 'cpf'

#     def __str__(self) -> str:
#         return f'{self.first_name} {self.last_name}'    
from django.conf import settings


    
