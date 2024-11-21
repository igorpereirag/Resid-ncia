from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Colecao  # Modelo Colecao assumido
from rest_framework.authtoken.models import Token  # Importa o modelo Token para usar na autenticação

class ColecaoAPITestCase(APITestCase):

    def setUp(self):
       
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.other_user = User.objects.create_user(username='user2', password='pass123')

        
        self.colecao = Colecao.objects.create(nome='Minha Coleção', descricao='Descrição da coleção', colecionador=self.user)

        
        self.colecao_list_url = '/api/colecao/'  
        self.colecao_detail_url = f'/api/colecao/{self.colecao.id}/'  

        
        self.token_user1 = Token.objects.create(user=self.user)
        self.token_user2 = Token.objects.create(user=self.other_user)

    def get_auth_headers(self, user_token):
        
        return {
            'Authorization': f'Token {user_token.key}'
        }

    def test_criar_colecao_usuario_autenticado(self):
        
        headers = self.get_auth_headers(self.token_user1)
        data = {'nome': 'Nova Coleção', 'descricao': 'Descrição da nova coleção'}
        response = self.client.post(self.colecao_list_url, data, HTTP_AUTHORIZATION=headers['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], 'Nova Coleção')
        self.assertEqual(response.data['colecionador'], self.user.id)

    def test_criar_colecao_usuario_nao_autenticado(self):
        
        data = {'nome': 'Coleção Não Autenticada', 'descricao': 'Descrição da coleção'}
        response = self.client.post(self.colecao_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_editar_colecao_propria(self):
        
        headers = self.get_auth_headers(self.token_user1)
        data = {'nome': 'Coleção Editada', 'descricao': 'Descrição atualizada'}
        response = self.client.put(self.colecao_detail_url, data, HTTP_AUTHORIZATION=headers['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Coleção Editada')

    def test_editar_colecao_outro_usuario(self):
        
        headers = self.get_auth_headers(self.token_user2)
        data = {'nome': 'Coleção Não Autorizada', 'descricao': 'Tentativa de edição'}
        response = self.client.put(self.colecao_detail_url, data, HTTP_AUTHORIZATION=headers['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deletar_colecao_propria(self):
        
        headers = self.get_auth_headers(self.token_user1)
        response = self.client.delete(self.colecao_detail_url, HTTP_AUTHORIZATION=headers['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Colecao.objects.filter(id=self.colecao.id).exists())

    def test_deletar_colecao_outro_usuario(self):
       
        headers = self.get_auth_headers(self.token_user2)
        response = self.client.delete(self.colecao_detail_url, HTTP_AUTHORIZATION=headers['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listar_colecoes_usuario_autenticado(self):
       
        headers = self.get_auth_headers(self.token_user1)
        response = self.client.get(self.colecao_list_url, HTTP_AUTHORIZATION=headers['Authorization'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_listar_colecoes_usuario_nao_autenticado(self):
        
        response = self.client.get(self.colecao_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

