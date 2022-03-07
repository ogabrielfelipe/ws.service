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
    return cadastra_setor()


@setor.route('/Setor/Atualizar/<int:codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_setor(codigo):
    return atualiza_setor(codigo)


@setor.route('/Setor/BuscaSetor/<int:codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_setor(codigo):
    return busca_setor(codigo)


@setor.route('/Setor/BuscaSetores', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_setores():
    return busca_setores()


@setor.route('/Setor/Excluir/<int:codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def excluir_setor(codigo):
    return delete_setor(codigo)

