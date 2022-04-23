from flask import Blueprint
from flask_jwt_extended import jwt_required
import datetime
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    JWTManager,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies
)
from ...controller.relatorio.AtendimentoRelatorio import  (
    relatorio_atendimento_ordem_data
)
from flask_cors import CORS

atendRel = Blueprint('atendRel', __name__)
CORS(atendRel)


@atendRel.route('/Relatorio/AtendimentoOrdemData', methods=['POST'])
@jwt_required(locations=["headers"])
def route_relatorio_atendimento_ordem_data():
    token_client = get_jwt()
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if datetime.datetime.now() >= exp-datetime.timedelta(minutes=10):
        access_token = create_access_token(identity=identity, fresh=True)
    response = relatorio_atendimento_ordem_data(usuario_logado=identity['id'])
    response[0].headers['token_access'] = access_token
    response[0].headers['Access-Control-Expose-Headers'] = 'token_access'
    return response[0], response[1]