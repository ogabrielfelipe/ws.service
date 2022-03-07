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
    current_user = get_jwt_identity()
    print('Usuário: ', current_user)

    return cadastra_solicitante()


@soli.route('/Solicitante/Alterar/<codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_solicitante(codigo):
    return atualiza_cadastro(codigo)


@soli.route('/Solicitante/BuscaSolicitante/<codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_Solicitante(codigo):
    return busca_solicitante(codigo)


@soli.route('/Solicitante/BuscaSolicitantes', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_Solicitantes():
    return busca_solicitantes()


@soli.route('/Solicitante/Excluir/<codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def exclui_solicitante(codigo):
    return delete_solicitante(codigo)
