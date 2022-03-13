from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controller.AtendimentoController import (
    cadastra_atendimento,
    atualiza_atendimento,
    busca_atendimento,
    busca_atendimentos,
    delete_atendimento
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


atend = Blueprint('atend', __name__)


@atend.route('/Atendimento/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cad_atendimento():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = cadastra_atendimento(usuario=get_jwt_identity())
    response.headers['token_access'] = access_token
    return response




@atend.route('/Atendimento/Alterar/<codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_atendimento(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = atualiza_atendimento(codigo)
    response.headers['token_access'] = access_token
    return response



@atend.route('/Atendimento/BuscaAtendimento/<codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_atendimento(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_atendimento(codigo)
    response.headers['token_access'] = access_token
    return response


'''
    Consulta atendimento não finalizada
    Montar a consulta com inner join, pegando as informações das outras tabelas
'''
@atend.route('/Atendimento/BuscaAtendimentos', methods=['POST'])
@jwt_required(locations=["headers"])
def busc_atendimentos():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_atendimentos()
    response.headers['token_access'] = access_token
    return response


@atend.route('/Atendimento/Excluir/<codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def excluir_atendimento(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = delete_atendimento(codigo)
    response.headers['token_access'] = access_token
    return response
