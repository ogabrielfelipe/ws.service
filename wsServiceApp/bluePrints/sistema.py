from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controller.SistemaController import (
    busca_sistema,
    busca_sistemas,
    cadastra_sistema,
    atualiza_sistema,
    delete_sistema
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

sist = Blueprint('sist', __name__)


@sist.route('/Sistema/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cad_sistema():
    return cadastra_sistema()


@sist.route('/Sistema/Alterar/<codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_sistema(codigo):
    return atualiza_sistema(codigo)


@sist.route('/Sistema/BuscaSistema/<codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_sistema(codigo):
    return busca_sistema(codigo)


@sist.route('/Sistema/BuscaSistemas', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_sistemas():
    return busca_sistemas()


@sist.route('/Sistema/Excluir/<codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def excluir_sistema(codigo):
    return delete_sistema(codigo)
