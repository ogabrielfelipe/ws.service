from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controller.SolicitanteController import (
    cadastra_solicitante,
    busca_solicitante,
    atualiza_cadastro,
    busca_solicitantes,
    delete_solicitante
)
from datetime import datetime
from datetime import timezone, timedelta
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    JWTManager,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies
)


soli = Blueprint('soli', __name__)


@soli.route('/Solicitante/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cad_solicitante():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = cadastra_solicitante()
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@soli.route('/Solicitante/Alterar/<codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_solicitante(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = atualiza_cadastro(codigo)
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@soli.route('/Solicitante/BuscaSolicitante/<codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_Solicitante(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_solicitante(codigo)
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@soli.route('/Solicitante/BuscaSolicitantes', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_Solicitantes():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_solicitantes()
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@soli.route('/Solicitante/Excluir/<codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def exclui_solicitante(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = delete_solicitante(codigo)
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response
