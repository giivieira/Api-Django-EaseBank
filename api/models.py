from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


#Criando os campos que devem ser preenchidos para criar a conta do usuário

#max_length -> tamanho máximo do elemento (caracteres)
#Unique = True -> não permite que o dado se repita

class Cliente(models.Model):
    nome = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    nascimento = models.DateField(null=True)
    telefone = models.CharField(max_length=11, unique=True)
    rg = models.CharField(max_length=11, unique=True)
    ruaResidencia = models.CharField(max_length=255)
    numeroResidencia = models.CharField(max_length=255)
    bairroResidencia = models.CharField(max_length=255)
    cepResidencia = models.IntegerField()
    estadoResidencia = models.CharField(max_length=255)
    cidadeResidencia = models.CharField(max_length=255)


    #Cria, salva e retorna um novo usuário
    class UserManager(BaseUserManager):
        def create_user(self, email, password=None, **extra_fields):
            if not email:
                raise ValueError("O usuário precisa ter um email")
        
            user = self.model(email=self.normalize_email(email), **extra_fields)
            user.set_password(password)
            user.save()
            return user