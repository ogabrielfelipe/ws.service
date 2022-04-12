from ..model.Usuario import db
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token
from ..model.Usuario import Usuario, usuario_schema, usuarios_schema
from werkzeug.security import generate_password_hash, check_password_hash
from .util import convert_pesquisa_consulta
from sqlalchemy import text


def cadastra_usuario():
    resp = request.get_json()
    senha = generate_password_hash(resp['senha'])
    user = Usuario(username=resp['username'], email=resp['email'],nome=resp['nome'], acesso=resp['acesso'], senha=senha)

    try:
        db.session.add(user)
        db.session.commit()
        result = usuario_schema.dump(user)
        return jsonify({'message': 'Usuário Cadastrado com sucesso', 'dado': result, 'error': ''}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Usuário não Cadastrado', 'dado': {},
                        'error': str(e)}), 500


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
        return jsonify({'message': 'Usuário não encontrado', 'dados': {}, 'error': ''}), 404

    try:
        user.username = username
        user.nome = nome
        user.senha = senha
        user.acesso = acesso
        db.session.commit()
        result = usuario_schema.dumps(user)
        return jsonify({'message': 'Usuário atualizado', 'dados': result, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}, 'error': str(e)}), 500


def busca_usuarios():
    resp = request.get_json()    
    convert_dict_search = convert_pesquisa_consulta(resp)
    try:
        sql_usuarios = text(f"""
            SELECT usuario.id, usuario.username, usuario.nome, usuario.email, usuario.acesso FROM USUARIO AS usuario
            {convert_dict_search}
            ORDER BY usuario.id
             """)
        consultaUsuarios = db.session.execute(sql_usuarios).fetchall()
        consultaUsuarios_dict = [dict(u) for u in consultaUsuarios]
        return jsonify({'msg': 'Busca efetuada com sucesso', 'dados': consultaUsuarios_dict, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Nao foi efetuado a busca com sucesso', 'dados': {}, 'error': str(e)}), 500


def atualiza_senha_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        resp = request.get_json()
        senhaAtual = resp['senhaAtual']
        senhaNova = resp['senhaNova']
        if usuario.senha == senhaAtual:
            try:
                usuario.senha=senhaNova
                db.session.commit()
                result = usuario_schema.dump(usuario)
                return jsonify({'msg': 'Senha do usuario alterada com sucesso', 'dados': result, 'error': ''}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'msg': 'Nao foi possivel alterar a senha', 'dados': '', 'error': str(e)}), 500
        else:
            return jsonify({'msg': 'Senha atual nao confere com a que esta salva no banco', 'dados': {}, 'error': ''}), 401
    else:
        return jsonify({'msg': 'Usuario nao encontrado', 'dados': {}, 'error': ''}), 404


def busca_usuario(id):
    user = Usuario.query.get(id)
    if user:
        result = usuario_schema.dump(user)
        return jsonify({'message': 'Sucesso', 'dados': result, 'error': ''}), 200
    return jsonify({'message': 'Usuários não encontrado', 'dados': {}, 'error': ''}), 404


def delete_usuario(id):
    user = Usuario.query.get(id)
    if not user:
        return jsonify({'message': 'Usuário não encontrado', 'dados': {}, 'error': ''}), 404

    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            result = usuario_schema.dump(user)
            return jsonify({'message': 'Usuário excluido', 'dados': result, 'error': ''}), 200
        except Exception as e:
            return jsonify({'message': 'Não foi possível exvluir', 'dados': {}, 'error': str(e)}), 500
