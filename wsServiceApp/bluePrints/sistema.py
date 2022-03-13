from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controller.SistemaController import (
    busca_sistema,
    busca_sistemas,
    cadastra_sistema,
    atualiza_sistema,
    delete_sistema
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

sist = Blueprint('sist', __name__)


@sist.route('/Sistema/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cad_sistema():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = cadastra_sistema()
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@sist.route('/Sistema/Alterar/<codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_sistema(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = atualiza_sistema(codigo)
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@sist.route('/Sistema/BuscaSistema/<codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_sistema(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_sistema(codigo)
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@sist.route('/Sistema/BuscaSistemas', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_sistemas():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_sistemas()
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@sist.route('/Sistema/Excluir/<codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def excluir_sistema(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = delete_sistema(codigo)
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response
