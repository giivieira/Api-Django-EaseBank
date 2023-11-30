from django.urls import path, include
from . import views 
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('contas', views.ContaView)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    # path('clientes/', views.listar_clientes),
    # path('usuarios/', views.ClientesView.as_view()),
    # path('usuario/<int:pk>', views.ClientesDetailView.as_view()),
    # path('conta/', views.exibir_conta),
]
