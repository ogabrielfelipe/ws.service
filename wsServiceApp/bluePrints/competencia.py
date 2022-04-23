import datetime
from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controller.CompetenciaController import (
    cadastra_competencia,
    busca_competencias,
    altera_trava_competencia,
    delete_competencia,
    listar_competencias
)
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
from flask_cors import CORS


comp = Blueprint('comp', __name__)


CORS(comp)


@comp.route('/Competencia/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cad_competencia():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = cadastra_competencia(usuario=get_jwt_identity())
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]


@comp.route('/Competencia/AlterarTrava/<int:codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_trava_competencia(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = altera_trava_competencia(codigo)
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]


@comp.route('/Competencia/BuscaCompetencias', methods=['POST'])
@jwt_required(locations=["headers"])
def busc_competencias():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_competencias()
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]


@comp.route('/Competencia/ListarCompetencias', methods=['POST'])
@jwt_required(locations=["headers"])
def lista_competencias():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])    
    identity = get_jwt_identity()
    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = listar_competencias()
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]


@comp.route('/Competencia/Excluir/<int:codigo>', methods=['DELETE'])
@jwt_required(locations=["headers"])
def exclui_competencia(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = delete_competencia(codigo)
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]
