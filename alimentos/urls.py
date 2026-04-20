from .views import AlimentoView
from django.urls import path

urlpatterns = [
   path('alimentos/',AlimentoView.as_view()), 
]

 