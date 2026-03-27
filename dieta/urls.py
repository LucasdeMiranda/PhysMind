from django.urls import path
from .views import DietaView

urlpatterns = [
    path('dieta/',DietaView.as_view()),
]
