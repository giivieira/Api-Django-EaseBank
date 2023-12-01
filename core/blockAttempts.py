from typing import Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, CPF_CNPJ=None, password=None, **kwargs):
        User = get_user_model()
        
        try:
            user = User.objects.get(CPF_CNPJ=CPF_CNPJ)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            # A senha está correta. Reinicie a contagem de tentativas.
            user.failed_login_attempts_count = 0
            if not user.is_active and user.blocked_at:
                reactivation_period = timedelta(minutes=1)
                if timezone.now() - user.blocked_at > reactivation_period:
                    user.is_active = True
                    user.blocked_at = None

            user.save()
            return user
        else:
            # A senha está incorreta. Incremente a contagem de tentativas.
            user.failed_login_attempts_count += 1
            user.save()
            
            # Verifique se a conta deve ser bloqueada.
            if user.failed_login_attempts_count >= 3:
                user.is_active = False
                user.blocked_at = timezone.now()
                user.save()
            
            return None
        
        
