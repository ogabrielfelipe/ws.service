import datetime
from sqlite3 import Date
from flask import Blueprint, request, jsonify
from ...controller.UsuarioController import autentica_usuario
from jwt import decode
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    JWTManager,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    unset_jwt_cookies
)
aut = Blueprint('auth', __name__)
jwt = JWTManager()


@aut.route('/Auth/Login', methods=['POST'])
def login():
    resp = request.get_json()
    token = autentica_usuario(username=resp['username'], senha=resp['senha'])
    if token is None:
        return jsonify({'message': 'Token não gerado', 'Token': {}}), 404
    return jsonify({"msg": "login successful", 'token_access': token}), 200


@aut.route("/Auth/Refresh", methods=["GET"])
@jwt_required(fresh=True)
def refresh():
    token_client = get_jwt()
    nbf = datetime.datetime.fromtimestamp(token_client['nbf'])
    exp = datetime.datetime.fromtimestamp(token_client['exp'])
    
    identity = get_jwt_identity()

    access_token = ''
    if exp <= nbf+datetime.timedelta(minutes=50):
        access_token = create_access_token(identity=identity, fresh=True)
    usuario = {
        "nome": identity['nome'],
        "username": identity['username'],
        "acesso": identity['acesso'],
        "email": identity['email']
    }
    return jsonify({"access_token": access_token, "usuario": usuario}), 200
