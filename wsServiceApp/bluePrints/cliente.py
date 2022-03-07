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


client = Blueprint('client', __name__)


@client.route('/Cliente/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cad_cliente():
    return cadastra_cliente()


@client.route('/Cliente/BuscaCliente/<codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_cliente(codigo):
    return busca_cliente(codigo)


@client.route('/Cliente/BuscaClientes', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_clientes():
    return busca_clientes()


@client.route('/Cliente/Alterar/<int:codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_cliente(codigo):
    print(codigo)
    return atualiza_cliente(codigo)


@client.route('/Cliente/Excluir/<codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def excluir_cliente(codigo):
    return delete_cliente(codigo)
