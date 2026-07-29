from django.urls import path
from .views import DietaView,ConsumoAlimentoDetailView,ConsumoAlimentoView,RefeicoesView,RefeicaoDetailView,DietaCreateView

urlpatterns = [
    path('dieta/',DietaView.as_view()),
    path('consumos/', ConsumoAlimentoView.as_view()),
    path('consumos/<int:pk>/', ConsumoAlimentoDetailView.as_view()),
    path('refeicoes/', RefeicoesView.as_view()),
    path('refeicoes/<int:pk>/', RefeicaoDetailView.as_view()),
    path('dietas/', DietaCreateView.as_view()),
    
]
