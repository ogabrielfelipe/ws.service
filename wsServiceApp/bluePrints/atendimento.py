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
    return cadastra_atendimento(usuario=get_jwt_identity())


@atend.route('/Atendimento/Alterar/<codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_atendimento(codigo):
    return atualiza_atendimento(codigo)


@atend.route('/Atendimento/BuscaAtendimento/<codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_atendimento(codigo):
    return busca_atendimento(codigo)


'''
    Consulta atendimento não finalizada
    Montar a consulta com inner join, pegando as informações das outras tabelas
'''
@atend.route('/Atendimento/BuscaAtendimentos', methods=['POST'])
@jwt_required(locations=["headers"])
def busc_atendimentos():
    return busca_atendimentos()


@atend.route('/Atendimento/Excluir/<codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def excluir_atendimento(codigo):
    return delete_atendimento(codigo)
