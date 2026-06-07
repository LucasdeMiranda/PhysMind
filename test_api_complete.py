"""
Testes automatizados para fluxo completo:
1. Login do usuário e obtenção de token
2. Inserção de alimento na dieta
3. Deleção de alimento da dieta
"""

import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from dieta.models import Dieta, Refeicao, ConsumoAlimento
from alimentos.models import AlimentoBase, AlimentoCustomizado
from usuarios.models import Perfil


class UsuarioAuthTestCase(APITestCase):
    """Testes de autenticação e login"""

    def setUp(self):
        self.client = APIClient()
        self.email = 'testuser@test.com'
        self.senha = 'senha123'

    def test_criar_novo_usuario_e_obter_token(self):
        """Teste 1: Criar novo usuário e obter token JWT"""
        response = self.client.post(
            '/api/cria-usuario/',
            {
                'email': self.email,
                'senha': self.senha
            },
            format='json'
        )

        # Verificar se status é 201 (created) para novo usuário
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verificar se token de acesso foi retornado
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['status'], 'novo')
        self.assertEqual(response.data['mensagem'], 'Usuário criado com sucesso')

        # Guardar token para próximos testes
        self.token_access = response.data['access']
        self.token_refresh = response.data['refresh']

    def test_login_usuario_existente(self):
        """Teste 2: Fazer login com usuário existente"""
        # Primeiro cria o usuário
        self.client.post(
            '/api/cria-usuario/',
            {
                'email': self.email,
                'senha': self.senha
            },
            format='json'
        )

        # Agora faz login novamente
        response = self.client.post(
            '/api/cria-usuario/',
            {
                'email': self.email,
                'senha': self.senha
            },
            format='json'
        )

        # Deve retornar 200 (OK) para usuário existente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'existente')
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_com_senha_incorreta(self):
        """Teste 3: Tentar login com senha incorreta"""
        # Cria usuário
        self.client.post(
            '/api/cria-usuario/',
            {
                'email': self.email,
                'senha': self.senha
            },
            format='json'
        )

        # Tenta login com senha errada
        response = self.client.post(
            '/api/cria-usuario/',
            {
                'email': self.email,
                'senha': 'senhaerrada'
            },
            format='json'
        )

        # Deve retornar 401 (Unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_perfil_criado_apos_login(self):
        """Teste 4: Verificar se perfil foi criado após login"""
        response = self.client.post(
            '/api/cria-usuario/',
            {
                'email': self.email,
                'senha': self.senha
            },
            format='json'
        )

        # Buscar usuário criado
        user = User.objects.get(username=self.email)
        # Verificar se perfil foi criado (get_or_create é chamado na view)
        perfil, created = Perfil.objects.get_or_create(usuario=user)

        # Verificar se perfil existe
        self.assertIsNotNone(perfil)
        self.assertEqual(perfil.usuario.email, self.email)


class AlimentoDietaTestCase(APITestCase):
    """Testes para inserção e deleção de alimentos na dieta"""

    def setUp(self):
        """Preparar dados para os testes"""
        self.client = APIClient()

        # Criar usuário e fazer login
        email = 'testuser@test.com'
        senha = 'senha123'

        response = self.client.post(
            '/api/cria-usuario/',
            {
                'email': email,
                'senha': senha
            },
            format='json'
        )

        self.token_access = response.data['access']
        self.user = User.objects.get(username=email)

        # Autenticar cliente com token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_access}')

        # Criar dieta ativa para o usuário
        self.dieta = Dieta.objects.create(
            usuario=self.user,
            calorias=2000,
            proteinas=150,
            carboidratos=200,
            gordura=70,
            ativo=True
        )

        # Criar refeição para a dieta
        self.refeicao = Refeicao.objects.create(
            usuario=self.user,
            dieta=self.dieta,
            nome='Almoço'
        )

        # Criar alimento base (banco de dados de alimentos)
        self.alimento_base = AlimentoBase.objects.create(
            nome='Frango',
            calorias=165,
            proteinas=31,
            carboidratos=0,
            fibra=0,
            sodio=74
        )

    def test_buscar_dieta_ativa(self):
        """Teste 5: Buscar dieta ativa do usuário autenticado"""
        response = self.client.get('/api/dieta/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.dieta.id)
        self.assertEqual(response.data['calorias'], 2000)

    def test_inserir_alimento_em_refeicao(self):
        """Teste 6: Inserir um alimento na dieta (via ConsumoAlimento)"""
        response = self.client.post(
            '/api/consumos/',
            {
                'alimentobase': self.alimento_base.id,
                'quantidade': 100,  # 100 gramas
                'refeicao': self.refeicao.id
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

        # Verificar se consumo foi criado no banco
        consumo = ConsumoAlimento.objects.filter(usuario=self.user).first()
        self.assertIsNotNone(consumo)
        self.assertEqual(consumo.alimentobase, self.alimento_base)
        self.assertEqual(consumo.quantidade, 100)

    def test_inserir_alimento_calcula_nutrientes(self):
        """Teste 7: Verificar se nutrientes são calculados corretamente"""
        response = self.client.post(
            '/api/consumos/',
            {
                'alimentobase': self.alimento_base.id,
                'quantidade': 100,
                'refeicao': self.refeicao.id
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Alimento tem 165 calorias por 100g, então 100g = 165 calorias
        self.assertEqual(response.data['calorias'], 165)
        # Alimento tem 31g proteína por 100g, então 100g = 31g proteína
        self.assertEqual(response.data['proteinas'], 31)
        # Frango tem 0g carboidratos
        self.assertEqual(response.data['carboidratos'], 0)

    def test_deletar_alimento_da_dieta(self):
        """Teste 8: Deletar um alimento da dieta"""
        # Primeiro insere o alimento
        response_create = self.client.post(
            '/api/consumos/',
            {
                'alimentobase': self.alimento_base.id,
                'quantidade': 100,
                'refeicao': self.refeicao.id
            },
            format='json'
        )

        consumo_id = response_create.data['id']

        # Agora deleta o alimento
        response_delete = self.client.delete(f'/api/consumos/{consumo_id}/')

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

        # Verificar se foi realmente deletado
        consumo_existe = ConsumoAlimento.objects.filter(id=consumo_id).exists()
        self.assertFalse(consumo_existe)

    def test_listar_alimentos_consumidos(self):
        """Teste 9: Listar todos os alimentos consumidos"""
        # Inserir 2 alimentos
        self.client.post(
            '/api/consumos/',
            {
                'alimentobase': self.alimento_base.id,
                'quantidade': 100,
                'refeicao': self.refeicao.id
            },
            format='json'
        )

        # Criar outro alimento
        alimento2 = AlimentoBase.objects.create(
            nome='Arroz',
            calorias=130,
            proteinas=2.7,
            carboidratos=28,
            fibra=0.4,
            sodio=1
        )

        self.client.post(
            '/api/consumos/',
            {
                'alimentobase': alimento2.id,
                'quantidade': 150,
                'refeicao': self.refeicao.id
            },
            format='json'
        )

        # Listar consumos
        response = self.client.get('/api/consumos/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_refeicao_sem_dieta_ativa_falha(self):
        """Teste 10: Criar refeição sem dieta ativa deve falhar"""
        # Desativar a dieta
        self.dieta.ativo = False
        self.dieta.save()

        response = self.client.post(
            '/api/consumos/',
            {
                'alimentobase': self.alimento_base.id,
                'quantidade': 100,
                'refeicao': self.refeicao.id
            },
            format='json'
        )

        # Deve retornar erro
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FluxoCompletoTestCase(APITestCase):
    """Teste do fluxo completo: Login → Inserir → Deletar"""

    def test_fluxo_completo_login_inserir_deletar(self):
        """
        Teste 11: Fluxo completo
        1. Login do usuário
        2. Inserir novo alimento na dieta
        3. Deletar o alimento
        """
        client = APIClient()

        # PASSO 1: Login
        email = 'fluxocompleto@test.com'
        senha = 'senhafluxo123'

        response_login = client.post(
            '/api/cria-usuario/',
            {
                'email': email,
                'senha': senha
            },
            format='json'
        )

        self.assertEqual(response_login.status_code, status.HTTP_201_CREATED)
        token = response_login.data['access']

        # Autenticar com token
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Buscar usuário
        user = User.objects.get(username=email)

        # Criar dieta e refeição
        dieta = Dieta.objects.create(
            usuario=user,
            calorias=2500,
            proteinas=180,
            carboidratos=250,
            gordura=80,
            ativo=True
        )

        refeicao = Refeicao.objects.create(
            usuario=user,
            dieta=dieta,
            nome='Café da Manhã'
        )

        # Criar alimento
        alimento = AlimentoBase.objects.create(
            nome='Ovos',
            calorias=155,
            proteinas=13,
            carboidratos=1.1,
            fibra=0,
            sodio=124
        )

        # PASSO 2: Inserir alimento na dieta
        response_insert = client.post(
            '/api/consumos/',
            {
                'alimentobase': alimento.id,
                'quantidade': 50,
                'refeicao': refeicao.id
            },
            format='json'
        )

        self.assertEqual(response_insert.status_code, status.HTTP_201_CREATED)
        consumo_id = response_insert.data['id']

        # Verificar se o alimento foi inserido
        consumo = ConsumoAlimento.objects.get(id=consumo_id)
        self.assertEqual(consumo.quantidade, 50)
        self.assertEqual(consumo.alimentobase.nome, 'Ovos')

        # PASSO 3: Deletar o alimento
        response_delete = client.delete(f'/api/consumos/{consumo_id}/')

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

        # Verificar se foi realmente deletado
        consumo_existe = ConsumoAlimento.objects.filter(id=consumo_id).exists()
        self.assertFalse(consumo_existe)
