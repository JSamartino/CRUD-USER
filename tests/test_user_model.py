"""
Testes unitários para o modelo User
"""
import pytest
from datetime import datetime
from app.models.user import User
from app import db
#Testando o model 
class TestUserModel:
    #Testar criação de um usuário
    def test_user_creation(self, app):
        with app.app_context():
            user = User(
                name='João Silva',
                email='joao@example.com',
                phone='11999999999'
            )
            
            assert user.name == 'João Silva'
            assert user.email == 'joao@example.com'
            assert user.phone == '11999999999'
            assert user.enabled == True
            assert user.created_at is not None
    
    
    def test_user_email_validation(self, app):
        with app.app_context():
            # Email válido
            user = User(name='João', email='joao@example.com')
            assert user.email == 'joao@example.com'
            
            # Email inválido
            with pytest.raises(ValueError, match='Formato de email inválido'):
                User(name='João', email='email-invalido')
            
            # Email vazio
            with pytest.raises(ValueError, match='Email é obrigatório'):
                User(name='João', email='')
    
    #Validação de nome
    def test_user_name_validation(self, app):
        with app.app_context():
            # Nome válido
            user = User(name='João Silva', email='joao@example.com')
            assert user.name == 'João Silva'
            
            # Nome vazio
            with pytest.raises(ValueError, match='Nome deve ter pelo menos 2 caracteres'):
                User(name='', email='joao@example.com')
    
    #Validação de telefone
    def test_user_phone_validation(self, app):
        with app.app_context():
            # Telefone válido
            user = User(name='João', email='joao@example.com', phone='11999999999')
            assert user.phone == '11999999999'
            
            # Telefone muito curto
            with pytest.raises(ValueError, match='Telefone deve ter pelo menos 10 dígitos'):
                User(name='João', email='joao@example.com', phone='123')
            
    
    #Testa conversão para dicionario
    def test_user_to_dict(self, app):
        with app.app_context():
            user = User(
                name='João Silva',
                email='joao@example.com',
                phone='11999999999'
            )
            
            user_dict = user.to_dict()
            
            assert user_dict['name'] == 'João Silva'
            assert user_dict['email'] == 'joao@example.com'
            assert user_dict['phone'] == '11999999999'
            assert user_dict['enabled'] == True
            assert 'id' in user_dict
            assert 'created_at' in user_dict
            assert 'updated_at' in user_dict
    

    def test_user_update_from_dict(self, app):
        with app.app_context():
            user = User(
                name='João Silva',
                email='joao@example.com',
                phone='11999999999'
            )
            
            update_data = {
                'name': 'João Santos',
                'email': 'joao.santos@example.com',
                'phone': '11888888888'
            }
            
            user.update_from_dict(update_data)
            
            assert user.name == 'João Santos'
            assert user.email == 'joao.santos@example.com'
            assert user.phone == '11888888888'
            assert user.updated_at is not None
    
    def test_user_repr(self, app):
        """Testa representação string do usuário"""
        with app.app_context():
            user = User(name='João Silva', email='joao@example.com')
            repr_str = repr(user)
            
            assert 'João Silva' in repr_str
            assert 'joao@example.com' in repr_str
