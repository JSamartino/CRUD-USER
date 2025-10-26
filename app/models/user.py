from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import validates
import re


class User(db.Model):
    
    __tablename__ = 'users'
    #Definindo o shema 
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=True)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    #Definindo o construtor
    def __init__(self, name, email, phone=None, enabled=True):
        self.name = name
        self.email = email
        self.phone = phone
        self.enabled = enabled
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
    #Validando os ampos  com @validates (email,nome e telefone)
    
    @validates('email')
    def validate_email(self, key, email):
        
        if not email:
            raise ValueError('Email é obrigatório')
        #Regex para validar o email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError('Formato de email inválido')
        
        return email.lower()
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError('Nome deve ter pelo menos 2 caracteres')
        
        if len(name) > 100:
            raise ValueError('Nome deve ter no máximo 100 caracteres')
        
        #Regex para validar o nome deixando somente com caracteres validos
        name_pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s\'-]+$'
        if not re.match(name_pattern, name):
            raise ValueError('Nome deve conter apenas letras')
        
        return name.strip()
    
    @validates('phone')
    def validate_phone(self, key, phone):
        if phone:
            # Verifica se contém apenas números
            if not re.match(r'^\d+$', phone):
                raise ValueError('Telefone deve conter apenas números')

            # Verifica tamanho mínimo
            if len(phone) < 10:
                raise ValueError('Telefone deve ter pelo menos 10 dígitos')
        
        return phone

    def to_dict(self):
        #Converte o objeto para dicionário
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_from_dict(self, data):
        #Atualiza o objeto a partir de um dicionário
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<User {self.name} ({self.email})>'
