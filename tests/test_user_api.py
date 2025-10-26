import pytest
import json
from app.models.user import User

class TestUserAPI:
    #Testando o get users com a lista vazia
    def test_get_all_users_empty(self, client):
        response = client.get('/api/users')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['data'] == []
        assert data['count'] == 0
    
    #Fazendo get com os dados de exemplo
    def test_get_all_users_with_data(self, client, sample_user):
        response = client.get('/api/users')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert len(data['data']) == 1
        assert data['count'] == 1
        assert data['data'][0]['name'] == 'João Samartino'
        assert data['data'][0]['email'] == 'joaossamartinos@gmail.com'
    
    #Testando o get users de acordo com o telefone 
    def test_get_user_by_phone_success(self, client, sample_user):
        response = client.get(f'/api/users/{sample_user.phone}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['data']['name'] == 'João Samartino'
        assert data['data']['email'] == 'joaossamartinos@gmail.com'
    
    #Testando com telefone não encontrado
    def test_get_user_by_phone_not_found(self, client):
        response = client.get('/api/phone/9999999999')
        assert response.status_code == 404
    
    #Testando create user
    def test_create_user_success(self, client):
        """Testa POST /users com sucesso"""
        user_data = {
            'name': 'Maria de Souza',
            'email': 'maria.souza@example.com',
            'phone': '11888888888'
        }
        
        response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['message'] == 'Usuário criado com sucesso'
        assert data['data']['name'] == 'Maria de Souza'
        assert data['data']['email'] ==  'maria.souza@example.com'
        assert data['data']['phone'] == '11888888888'
    
    #Testando o post sem os campos obrigatorios 
    def test_create_user_missing_required_fields(self, client):
        user_data = {
            'name': 'Julia Santos'
        }
        
        response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'Campo email é obrigatório' in data['message']
        
    #Testando com email invalido
    def test_create_user_invalid_email(self, client):
        user_data = {
            'name': 'Maria Santos',
            'email': 'email-invalido'
        }
        
        response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'Formato de email inválido' in data['message']
    
    #Testando com email duplicado
    def test_create_user_duplicate_email(self, client, sample_user):
        user_data = {
            'name': 'Maria Santos',
            'email': 'joaossamartinos@gmail.com'  # email já existe
        }
        
        response = client.post(
            '/api/users',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'Email já está em uso' in data['message']
    
    #Testar user sem envio de dados
    def test_create_user_no_json(self, client):
        response = client.post('/api/users')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'Dados JSON são obrigatórios' in data['message']
    
    #Testar update de user
    def test_update_user_success(self, client, sample_user):

        update_data = {
            'name': 'João Santos'
        }
        
        response = client.put(
            f'/api/users/{sample_user.phone}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['message'] == 'Usuário atualizado com sucesso'
        assert data['data']['name'] == 'João Santos'
        assert data['data']['email'] == 'joaossamartinos@gmail.com'  # não alterado
    
    #Testar update sem encontrar o telefone do usuário
    def test_update_user_not_found(self, client):
        update_data = {'name': 'João Santos'}
    
        response = client.put(
            '/api/users/999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    #Update com dois email
    def test_update_user_duplicate_email(self, client, sample_user):
        # Criar outro usuário
        user2 = User(name='Maria', email='maria@example.com')
        from app import db
        with client.application.app_context():
            db.session.add(user2)
            db.session.commit()
        
        update_data = {
            'email': 'maria@example.com'  # email já usado por outro usuário
        }
        
        response = client.put(
            f'/api/users/{sample_user.phone}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'E-mail já cadastrado' in data['message']
    
    #Teste de delete no user
    def test_delete_user_success(self, client, sample_user):
        response = client.delete(f'/api/users/{sample_user.phone}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['message'] == 'Usuário removido com sucesso'
        
        # Verificar se usuário foi marcado como inativo
        response = client.get('/api/users')
        data = json.loads(response.data)
        assert data['count'] == 0  # usuário inativo não aparece na lista
        
    #Apagando usuario sem o telefone
    def test_delete_user_not_found(self, client):
        response = client.delete('/api/users/999')
    
        assert response.status_code == 404
