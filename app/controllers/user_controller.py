from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError
from datetime import datetime

user_bp = Blueprint('users', __name__)

#Controller para realizar o CRUD de usuários
class UserController:
    
    #Retorna todos os usuários habilitados com enabled=true
    @staticmethod
    def get_all_users():
        try:
            users = User.query.filter_by(enabled=True).all()
            return jsonify({
                'success': True,
                'data': [user.to_dict() for user in users],
                'count': len(users)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro ao buscar usuários: {str(e)}'
            }), 500
            
            
    #Retorna um usuário específico por telefone
    @staticmethod
    def get_user_by_phone(phone):
        try:
            user = User.query.filter_by(phone=phone).first()
            if not user:
                return jsonify({
                    'success': False,
                    'message': f'Usuário com telefone {phone} não encontrado.'
                }), 404
                
            return jsonify({
                'success': True,
                'data': user.to_dict()
            }), 200

        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro ao buscar usuário: {str(e)}'
            }), 500
            
            
    @staticmethod
    def create_user():
        #Cria um novo usuário
        try:
            data = request.get_json(silent=True)
            
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Dados JSON são obrigatórios'
                }), 400
            
            # Validação de campos obrigatórios
            required_fields = ['name', 'email','phone']
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({
                        'success': False,
                        'message': f'Campo {field} é obrigatório'
                    }), 400
            
            # Verificar se email já existe
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'Email já está em uso'
                }), 409
            
            # Criar novo usuário
            user = User(
                name=data['name'],
                email=data['email'],
                phone=data.get('phone'),
                enabled=data.get('enabled', True)
            )
            
            db.session.add(user)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Usuário criado com sucesso',
                'data': user.to_dict()
            }), 201
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': 'Erro: Telefone já cadastrado'
            }), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao criar usuário: {str(e)}'
            }), 500
            
    @staticmethod        
    def update_user_by_phone(phone):
        try:
            # Buscar usuário pelo telefone
            user = User.query.filter_by(phone=phone).first()
            if not user:
                return jsonify({
                    'success': False,
                    'message': f'Usuário com telefone {phone} não encontrado'
                }), 404

            data = request.get_json(silent=True)
            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Dados JSON são obrigatórios'
                }), 400

            # Atualizar apenas nome e email (se forem informados)
            if 'name' in data:
                user.name = data['name']

            if 'email' in data:
                # Verifica se o novo email já existe em outro usuário
                existing_email = User.query.filter(
                    User.email == data['email'],
                    User.id != user.id
                ).first()
                if existing_email:
                    return jsonify({
                        'success': False,
                        'message': 'E-mail já cadastrado'
                    }), 409

                user.email = data['email']

            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Usuário atualizado com sucesso',
                'data': user.to_dict()
            }), 200

        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400

        except IntegrityError:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': 'Erro de integridade: e-mail já existe'
            }), 409

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao atualizar usuário: {str(e)}'
            }), 500
            
             
    @staticmethod
    def delete_user(phone):
        """Desabilita um usuário com base no telefone"""
        try:
            # Busca o usuário pelo telefone
            user = User.query.filter_by(phone=phone).first()
            if not user:
                return jsonify({
                    'success': False,
                    'message': f'Usuário com telefone {phone} não encontrado'
                }), 404

            # Desabilita o usuário
            user.enabled = False
            user.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Usuário removido com sucesso'
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao remover usuário: {str(e)}'
            }), 500
            
    #Reativar usuário que foi apagado        
    @staticmethod
    def restore_user(phone):
        try:
            # Busca o usuário pelo telefone (incluindo desabilitados)
            user = User.query.filter_by(phone=phone).first()
            if not user:
                return jsonify({
                    'success': False,
                    'message': f'Usuário com telefone {phone} não encontrado'
                }), 404
            
            # Verifica se já está habilitado
            if user.enabled:
                return jsonify({
                    'success': False,
                    'message': 'Usuário já está ativo'
                }), 400

            # Reativa o usuário
            user.enabled = True
            user.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Usuário reativado com sucesso',
                'data': user.to_dict()
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Erro ao reativar usuário: {str(e)}'
            }), 500
    

# Rotas da API
@user_bp.route('/users', methods=['GET'])
def get_users():
    return UserController.get_all_users()

@user_bp.route('/users/<string:phone>', methods=['GET'])
def get_user(phone):
    return UserController.get_user_by_phone(phone)

@user_bp.route('/users', methods=['POST'])
def create_user():
    return UserController.create_user()

@user_bp.route('/users/<string:phone>', methods=['PUT'])
def update_user(phone):
    return UserController.update_user_by_phone(phone)

@user_bp.route('/users/<string:phone>', methods=['DELETE'])
def delete_user(phone):
    return UserController.delete_user(phone)

@user_bp.route('/users/<string:phone>/restore', methods=['PATCH'])
def restore_user(phone):
    return UserController.restore_user(phone)



            
            