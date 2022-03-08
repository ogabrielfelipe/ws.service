from flask import Blueprint
from flask_jwt_extended import jwt_required
from wsServiceApp.controller.UsuarioController import (
    cadastra_usuario,
    atualiza_usuario,
    busca_usuarios,
    busca_usuario
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


user = Blueprint('user', __name__)


@user.route('/Usuario/Cadastrar', methods=['POST'])
@jwt_required(locations=["headers"])
def cadastra_user():
    return cadastra_usuario()


@user.route('/Usuario/Atualiza/<codigo>', methods=['PATCH'])
@jwt_required(locations=["headers"])
def atualiza_user(codigo):
    return atualiza_usuario(codigo)


@user.route('/Usuario/BuscaTodos', methods=['GET'])
@jwt_required(locations=["headers"])
def busca_todos():
    return busca_usuarios()


@user.route('/Usuario/BuscaUsurio/<codigo>', methods=['GET'])
@jwt_required(locations=["headers"])
def busca_user(codigo):
    return busca_usuario(codigo)
