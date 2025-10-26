"""
Configuração dos testes pytest
"""
import pytest
from flask import Flask
from app import db
from app.models.user import User

@pytest.fixture
def app():

    # Criar app
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False
    })
    
    # Importar e inicializar extensões
    from app import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints
    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

#Dados para exemplos de teste
@pytest.fixture
def sample_user_data():
    return {
        'name': 'João Samartino',
        'email': 'joaossamartinos@gmail.com',
        'phone': '16997113777',
        'enabled': True
    }

#Criando um usuário de teste
@pytest.fixture
def sample_user(app, sample_user_data):
    with app.app_context():
        user = User(**sample_user_data)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        # Reatachar o usuário à sessão para evitar DetachedInstanceError
        user = db.session.merge(user)
        return user
