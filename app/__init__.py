from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os 

# Iniciando as extensões 
db = SQLAlchemy()
migrate = Migrate()

def create_app(): 
    # Criando a aplicação
    app = Flask(__name__)

    # Configurando o banco de dados
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(basedir, "..", "instance")
    os.makedirs(instance_dir, exist_ok=True)   # 👈 garante que a pasta existe!

    db_path = os.path.join(instance_dir, "users.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Iniciando as extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrando blueprints
    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')
    
    # Criando as tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app
