from django.urls import path, include
from api import views 
from rest_framework.routers import DefaultRouter, SimpleRouter

from api import views

router = SimpleRouter()
router.register('contas', views.ContaView)
router.register('movimentacao', views.MovimentacaoViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    # path('clientes/', views.listar_clientes),
    # path('usuarios/', views.ClientesView.as_view()),
    # path('usuario/<int:pk>', views.ClientesDetailView.as_view()),
    # path('conta/', views.exibir_conta),
]
