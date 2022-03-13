from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controller.SetorControlller import (
    cadastra_setor,
    atualiza_setor,
    busca_setor,
    busca_setores,
    delete_setor
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

setor = Blueprint('setor', __name__)


@setor.route('/Setor/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cad_setor():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = cadastra_setor()
    response.headers['token_access'] = access_token
    return response


@setor.route('/Setor/Atualizar/<int:codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_setor(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = atualiza_setor(codigo)
    response.headers['token_access'] = access_token
    return response


@setor.route('/Setor/BuscaSetor/<int:codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_setor(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_setor(codigo)
    response.headers['token_access'] = access_token
    return response


@setor.route('/Setor/BuscaSetores', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_setores():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_setores()
    response.headers['token_access'] = access_token
    return response


@setor.route('/Setor/Excluir/<int:codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def excluir_setor(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = delete_setor(codigo)
    response.headers['token_access'] = access_token
    return response

