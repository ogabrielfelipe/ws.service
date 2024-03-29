import datetime
from flask import Blueprint
from flask_jwt_extended import jwt_required
from wsServiceApp.bluePrints.Login.auth import refresh
from ..controller.ClienteController import (
    cadastra_cliente,
    atualiza_cliente,
    busca_cliente,
    busca_clientes,
    delete_cliente
)
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

client = Blueprint('client', __name__)

CORS(client)

@client.route('/Cliente/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cad_cliente():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = cadastra_cliente()
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1] 


@client.route('/Cliente/BuscaCliente/<codigo>', methods=['POST'])
@jwt_required(locations=["headers"])
def busc_cliente(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_cliente(codigo)
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]


@client.route('/Cliente/BuscaClientes', methods=['POST'])
@jwt_required(locations=["headers"])
def busc_clientes():    
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_clientes()
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'

    return response[0], response[1]


@client.route('/Cliente/Alterar/<int:codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_cliente(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = atualiza_cliente(codigo)
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1] 


@client.route('/Cliente/Excluir/<codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def excluir_cliente(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])    
    identity = get_jwt_identity()
    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = delete_cliente(codigo)
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]
