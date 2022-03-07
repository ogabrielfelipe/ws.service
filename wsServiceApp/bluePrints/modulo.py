from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controller.ModuloController import (
    cadastra_modulo,
    atualiza_modulo,
    busca_modulo,
    busca_modulos,
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


mod = Blueprint('mod', __name__)



@mod.route('/Modulo/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cad_modulo():
    return cadastra_modulo()


@mod.route('/Modulo/Alterar/<codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_modulo(codigo):
    return atualiza_modulo(codigo)


@mod.route('/Modulo/BuscaModulo/<codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_modulo(codigo):
    return busca_modulo(codigo)


@mod.route('/Modulo/BuscaModulos', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_modulos():
    return busca_modulos()


@mod.route('/Modulo/Excluir/<codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def excluir_modulo(codigo):
    return delete_setor(codigo)
