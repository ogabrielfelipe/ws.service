import json
from ..model.Usuario import db
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token
from ..model.Usuario import Usuario, usuario_schema, usuarios_schema
from werkzeug.security import generate_password_hash, check_password_hash


def cadastra_usuario():
    resp = request.get_json()
    senha = generate_password_hash(resp['senha'])
    user = Usuario(username=resp['username'], nome=resp['nome'], acesso=resp['acesso'], senha=senha)

    try:
        db.session.add(user)
        db.session.commit()
        result = usuario_schema.dump(user)
        return jsonify({'message': 'Usuário Cadastrado com sucesso', 'dado': result}), 201
    except SQLAlchemyError as sa:
        db.session.rollback()
        return jsonify({'message': 'Usuário não Cadastrado', 'dado': {},
                        'Error': json.dumps(sa)}), 201


def usuario_username(username):
    try:
        return Usuario.query.filter(Usuario.username == username).one()
    except:
        return None


def autentica_usuario(username, senha):
    user = usuario_username(username)
    user_json = usuario_schema.dump(user)
    if user and check_password_hash(user.senha, senha):
        access_token = create_access_token(identity=user_json, fresh=True)
        return access_token
    else:
        return None


def identifica_usuario(payload):
    usuario_id = payload['identity']
    return Usuario.query.get(usuario_id)


def atualiza_usuario(id):
    resp = request.get_json()
    nome = resp['nome']
    username = resp['username']
    senha = generate_password_hash(resp['senha'])
    acesso = resp['acesso']

    user = Usuario.query.get(id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado', 'dados': {}}), 404

    try:
        user.username = username
        user.nome = nome
        user.senha = senha
        user.acesso = acesso
        db.session.commit()
        result = usuario_schema.dumps(user)
        return jsonify({'message': 'Usuário atualizado', 'dados': result}), 201
    except:
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}}), 500


def busca_usuarios():
    users = Usuario.query.all()
    if users:
        result = usuarios_schema.dump(users)
        return jsonify({'message': 'Sucesso', 'dados': result}), 200
    return jsonify({'message': 'Usuários não encontrado', 'dados': {}}), 404


def busca_usuario(id):
    user = Usuario.query.get(id)
    if user:
        result = usuario_schema.dump(user)
        return jsonify({'message': 'Sucesso', 'dados': result}), 200
    return jsonify({'message': 'Usuários não encontrado', 'dados': {}}), 404

def delete_usuario(id):
    user = Usuario.query.get(id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado', 'dados': {}}), 404

    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            result = usuario_schema.dump(user)
            return jsonify({'message': 'Usuário excluido', 'dados': result}), 200
        except:
            return jsonify({'message': 'Não foi possível exvluir', 'dados': {}}), 500
