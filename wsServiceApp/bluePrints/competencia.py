import datetime
from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controller.CompetenciaController import (
    cadastra_competencia,
    busca_competencia,
    busca_competencias,
    atualiza_competencia,
    altera_trava_competencia,
    delete_competencia,
    busca_competencia_mes,
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


comp = Blueprint('comp', __name__)


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
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@comp.route('/Competencia/Alterar/<int:codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def alter_competencia(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = atualiza_competencia(codigo)
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


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
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@comp.route('/Competencia/BuscaCompetencia/<int:codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_competencia(codigo):
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_competencia(codigo)
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@comp.route('/Competencia/BuscaCompetencias', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_competencias():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_competencias()
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@comp.route('/Competencia/BuscaCompetenciaMes', methods=['GET'])
@jwt_required(locations=["headers"])
def busc_mes_competencias():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = busca_competencia_mes()
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


@comp.route('/Competencia/ListarCompetencias', methods=['GET'])
@jwt_required(locations=["headers"])
def lista_competencias():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])    
    identity = get_jwt_identity()
    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = listar_competencias()
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response


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
    response.headers['token_access'] = access_token
    response.headers['Access-Control-Expose-Headers'] = 'token_access'
    return response
