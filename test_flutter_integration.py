"""
Testes de integração: Simulando requisições do Flutter para a API Django
Usa APIClient do Django para simular o cliente http do Flutter
"""

import json
import time
from django.test import TestCase
from django.contrib.auth.models import User
from dieta.models import Dieta, Refeicao, ConsumoAlimento
from alimentos.models import AlimentoBase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class FlutterMobileIntegrationTestCase(APITestCase):
    """Testes que simulam como o Flutter interage com a API"""

    def setUp(self):
        """Preparar dados e ambiente para os testes"""
        self.base_url = 'http://127.0.0.1:8000/api'
        self.client = APIClient()

    def test_fluxo_flutter_completo_login_and_diet_operations(self):
        """
        Teste 12: Simular fluxo completo do Flutter
        1. Cadastro/Login do usuário
        2. Buscar alimentos disponíveis
        3. Inserir alimento na dieta
        4. Listar alimentos consumidos
        5. Deletar alimento
        """

        email = 'flutter_user@test.com'
        senha = 'flutter_senha_123'

        # ETAPA 1: Login/Cadastro (como faria o Flutter)
        print("\n[FLUTTER] Fazendo login/cadastro...")
        response_login = self.client.post(
            '/api/cria-usuario/',
            {
                'email': email,
                'senha': senha
            },
            format='json'
        )

        self.assertEqual(response_login.status_code, status.HTTP_201_CREATED)
        access_token = response_login.data['access']
        refresh_token = response_login.data['refresh']

        print("OK Login bem-sucedido")
        print(f"  Access Token: {access_token[:20]}...")
        print(f"  Refresh Token: {refresh_token[:20]}...")

        # Autenticar cliente
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Buscar usuário criado
        user = User.objects.get(username=email)

        # Criar dieta ativa
        dieta = Dieta.objects.create(
            usuario=user,
            calorias=2000,
            proteinas=150,
            carboidratos=200,
            gordura=65,
            ativo=True
        )

        # ETAPA 2: Buscar dieta ativa
        print("\n[FLUTTER] Buscando dieta ativa...")
        response_dieta = self.client.get('/api/dieta/')

        self.assertEqual(response_dieta.status_code, status.HTTP_200_OK)
        print(f"OK Dieta encontrada: {response_dieta.data['calorias']} kcal")

        # ETAPA 3: Criar refeição
        print("\n[FLUTTER] Criando refeição...")
        response_refeicao = self.client.post(
            '/api/refeicoes/',
            {
                'nome': 'Almoço'
            },
            format='json'
        )

        self.assertEqual(response_refeicao.status_code, status.HTTP_201_CREATED)
        refeicao_id = response_refeicao.data['id']
        print(f"OK Refeição criada: ID {refeicao_id}")

        # ETAPA 4: Criar alimentos para teste
        print("\n[FLUTTER] Criando banco de alimentos...")
        alimentos_dados = [
            {'nome': 'Peito de Frango', 'calorias': 165, 'proteinas': 31, 'carboidratos': 0},
            {'nome': 'Batata Doce', 'calorias': 86, 'proteinas': 1.6, 'carboidratos': 20},
            {'nome': 'Brócolis', 'calorias': 34, 'proteinas': 2.8, 'carboidratos': 7},
        ]

        alimentos = []
        for alimento_data in alimentos_dados:
            alimento = AlimentoBase.objects.create(
                nome=alimento_data['nome'],
                calorias=alimento_data['calorias'],
                proteinas=alimento_data['proteinas'],
                carboidratos=alimento_data['carboidratos'],
                fibra=0,
                sodio=0
            )
            alimentos.append(alimento)
            print(f"OK Alimento criado: {alimento.nome}")

        # ETAPA 5: Inserir alimentos na dieta
        print("\n[FLUTTER] Inserindo alimentos na dieta...")
        consumos_ids = []

        for idx, alimento in enumerate(alimentos):
            response_consumo = self.client.post(
                '/api/consumos/',
                {
                    'alimentobase': alimento.id,
                    'quantidade': 100 + (idx * 50),  # Quantidades variadas
                    'refeicao': refeicao_id
                },
                format='json'
            )

            self.assertEqual(response_consumo.status_code, status.HTTP_201_CREATED)
            consumo_id = response_consumo.data['id']
            consumos_ids.append(consumo_id)

            print(f"OK {alimento.nome} ({response_consumo.data['quantidade']}g) - "
                  f"{response_consumo.data['calorias']} kcal")

        # ETAPA 6: Listar consumos
        print("\n[FLUTTER] Listando alimentos consumidos...")
        response_lista = self.client.get('/api/consumos/')

        self.assertEqual(response_lista.status_code, status.HTTP_200_OK)
        print(f"OK Total de alimentos na refeição: {len(response_lista.data)}")

        for consumo in response_lista.data:
            print(f"  - {consumo['nome']}: {consumo['quantidade']}g, "
                  f"{consumo['calorias']:.0f} kcal")

        # ETAPA 7: Deletar um alimento
        print("\n[FLUTTER] Deletando um alimento...")
        consumo_a_deletar = consumos_ids[0]

        response_delete = self.client.delete(f'/api/consumos/{consumo_a_deletar}/')

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        print(f"OK Alimento deletado com sucesso (ID: {consumo_a_deletar})")

        # ETAPA 8: Verificar se foi deletado
        print("\n[FLUTTER] Verificando se alimento foi deletado...")
        response_lista_final = self.client.get('/api/consumos/')

        self.assertEqual(response_lista_final.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_lista_final.data), len(alimentos) - 1)
        print(f"OK Total de alimentos agora: {len(response_lista_final.data)}")

    def test_token_refresh_flow(self):
        """Teste 13: Testar renovação de token (refresh)"""

        email = 'token_test@test.com'
        senha = 'token_senha_123'

        # Login
        response_login = self.client.post(
            '/api/cria-usuario/',
            {
                'email': email,
                'senha': senha
            },
            format='json'
        )

        refresh_token = response_login.data['refresh']

        # Testar refresh
        print("\n[FLUTTER] Renovando token...")
        response_refresh = self.client.post(
            '/api/token/refresh/',
            {
                'refresh': refresh_token
            },
            format='json'
        )

        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_refresh.data)
        print(f"OK Token renovado com sucesso")
        print(f"  Novo Access Token: {response_refresh.data['access'][:20]}...")

    def test_unauthorized_access_sem_token(self):
        """Teste 14: Tentar acessar endpoints sem token deve falhar"""

        print("\n[FLUTTER] Tentando acessar sem autenticação...")
        response = self.client.get('/api/dieta/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(f"OK Acesso bloqueado corretamente (401 Unauthorized)")

    def test_multiple_meals_in_day(self):
        """Teste 15: Criar múltiplas refeições em um dia"""

        email = 'meals_test@test.com'
        senha = 'meals_senha_123'

        # Login
        response_login = self.client.post(
            '/api/cria-usuario/',
            {
                'email': email,
                'senha': senha
            },
            format='json'
        )

        access_token = response_login.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        user = User.objects.get(username=email)

        # Criar dieta
        dieta = Dieta.objects.create(
            usuario=user,
            calorias=2500,
            proteinas=180,
            carboidratos=250,
            gordura=80,
            ativo=True
        )

        # Criar múltiplas refeições
        meals = ['Café da Manhã', 'Almoço', 'Lanche', 'Jantar']

        print("\n[FLUTTER] Criando múltiplas refeições...")
        for meal_name in meals:
            response = self.client.post(
                '/api/refeicoes/',
                {
                    'nome': meal_name
                },
                format='json'
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            print(f"OK Refeição '{meal_name}' criada")

        # Listar refeições
        response_list = self.client.get('/api/refeicoes/')
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_list.data), len(meals))
        print(f"OK Total de refeições: {len(response_list.data)}")
