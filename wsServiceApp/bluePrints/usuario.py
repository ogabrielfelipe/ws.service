from flask import Blueprint
from wsServiceApp.controller.UsuarioController import (
    cadastra_usuario,
    atualiza_usuario,
    busca_usuarios,
    busca_usuario,
    atualiza_senha_usuario,
    inativa_usuario,
    atualiza_senha_adm_usuario
)
import datetime
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    JWTManager,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies
)
from flask_cors import CORS


user = Blueprint('user', __name__)


CORS(user)


@user.route('/Usuario/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cadastra_user():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = cadastra_usuario()
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1] 


@user.route('/Usuario/Atualiza/<int:codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def atualiza_user(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = atualiza_usuario(codigo)
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]


@user.route('/Usuario/BuscaTodos', methods=['POST'])
@jwt_required(locations=["headers"])
def busca_todos():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_usuarios()
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]


@user.route('/Usuario/BuscaUsurio/<int:codigo>', methods=['POST'])
@jwt_required(locations=["headers"])
def busca_user(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_usuario(codigo)
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]


@user.route('/Usuario/AlteraSenha', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_senha_usuario():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()
    print(identity['id'])
    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = atualiza_senha_usuario(identity['id'])
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]


@user.route('/Usuario/Inativar/<int:codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def inativa_usuario_route(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = inativa_usuario(codigo)
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]


@user.route('/Usuario/AlteraSenhaAdm/<int:codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def inativa_usuario_adm_route(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = atualiza_senha_adm_usuario(codigo, identity['acesso'])
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]