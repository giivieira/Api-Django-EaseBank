"""
Models de toda a aplicaçãp
"""
import os
import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone
from django.conf import settings


def user_image_field(instance, filename):
    """Generate file path for new user image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'user', filename)

class Conta(models.Model):
    agencia = models.IntegerField()
    numero = models.IntegerField()
    digito = models.IntegerField()
    saldo = models.DecimalField(max_digits=20, decimal_places=2)
    limite = models.DecimalField(max_digits=20, decimal_places=2)
    chavePix = models.CharField(max_length=100, unique=True)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )

    def __str__(self) -> str:
        return self.cliente.first_name


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
    remetente = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name="remetente")
    remetenteNome = models.CharField(max_length=100)
    destinatario = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name="destinatario")
    destinatarioNome = models.CharField(max_length=100)
    chavePix = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default="p")
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=100)



class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fiels):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must be an email address")

        user = self.model(email=self.normalize_email(email), **extra_fiels)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """Create, save and return a new super user."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in system"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    cpf = models.CharField(max_length=11, unique=True, null=False)
    url_imagem = models.ImageField(null=True, upload_to=user_image_field)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    login_attempts = models.PositiveIntegerField(default=0)
    locked_at = models.DateTimeField(null=True, blank=True)
    unlocked_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'cpf'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'