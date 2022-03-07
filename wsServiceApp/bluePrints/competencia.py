from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controller.CompetenciaController import (
    cadastra_competencia,
    busca_competencia,
    busca_competencias,
    atualiza_competencia,
    altera_trava_competencia,
    delete_competencia
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


comp = Blueprint('comp', __name__)


@comp.route('/Competencia/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cad_competencia():
    return cadastra_competencia(usuario=get_jwt_identity())


@comp.route('/Competencia/Alterar/<int:codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_competencia(codigo):
    return atualiza_competencia(codigo)


@comp.route('/Competencia/AlterarTrava/<int:codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_trava_competencia(codigo):
    return altera_trava_competencia(codigo)


@comp.route('/Competencia/BuscaCompetencia/<int:codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_competencia(codigo):
    return busca_competencia(codigo)


@comp.route('/Competencia/BuscaCompetencias', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_competencias():
    return busca_competencias()


@comp.route('/Competencia/Excluir/<int:codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def exclui_competencia(codigo):
    return delete_competencia(codigo)
