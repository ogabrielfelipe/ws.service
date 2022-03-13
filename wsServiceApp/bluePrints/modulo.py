from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controller.ModuloController import (
    cadastra_modulo,
    atualiza_modulo,
    busca_modulo,
    busca_modulos,
    delete_modulo
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


mod = Blueprint('mod', __name__)



@mod.route('/Modulo/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cad_modulo():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = cadastra_modulo()
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@mod.route('/Modulo/Alterar/<codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_modulo(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = atualiza_modulo(codigo)
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@mod.route('/Modulo/BuscaModulo/<codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_modulo(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_modulo(codigo)
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@mod.route('/Modulo/BuscaModulos', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_modulos():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_modulos()
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@mod.route('/Modulo/Excluir/<codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def excluir_modulo(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = delete_modulo(codigo)
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response
