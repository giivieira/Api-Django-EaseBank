from django.utils import timezone
from core.models import User
from django.http import JsonResponse
from rest_framework import status
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from rest_framework import status
from django.core.handlers.wsgi import WSGIRequest
import json

class LoginAttemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        # Armazena o corpo da solicitação antes de ler de request.POST ou request.data
        body = request.body

        response = self.get_response(request)

        if request.path == '/api/token/':
            # Verifica o tipo de conteúdo da solicitação
            content_type = request.headers.get('Content-Type', '').lower()

            if 'application/json' in content_type:
                # Se o tipo de conteúdo for JSON
                try:
                    data = json.loads(body.decode('utf-8'))
                    cpf = data.get('cpf')
                except json.JSONDecodeError:
                    cpf = None
            elif 'application/x-www-form-urlencoded' in content_type:
                # Se o tipo de conteúdo for formulário
                cpf = request.POST.get('cpf')
            else:
                cpf = None

            if cpf:
                user = User.objects.filter(cpf=cpf).first()

                if user and response.status_code == status.HTTP_401_UNAUTHORIZED:
                    
                    user.login_attempts += 1
                    user.save()

                    if user.login_attempts >= 3:
                        user.locked_at = timezone.now()
                        user.unlocked_at = timezone.now() + timezone.timedelta(minutes=15)
                        user.save()

                        return JsonResponse(
                            {'detail': 'Sua conta foi bloqueada. Tente novamente após 15 minutos.'},
                            status=status.HTTP_401_UNAUTHORIZED
                        )

                if user and user.login_attempts >= 3 and user.locked_at != None and user.unlocked_at != None and status.HTTP_200_OK:
                    
                    if timezone.now() >= user.unlocked_at:
                        user.login_attempts = 0
                        user.locked_at = None
                        user.unlocked_at = None
                        user.save()
                    else:
                        return JsonResponse(
                            {'detail': 'Sua conta foi bloqueada. Tente novamente mais tarde.'},
                            status=status.HTTP_401_UNAUTHORIZED
                        )

        return response