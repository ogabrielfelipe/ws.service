from flask import Blueprint
from...controller.UsuarioController import cadUser
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required



user = Blueprint('user', __name__)

@user.route('/Usuario/Cadastrar', methods=['POST'])
@jwt_required()
def routeUser():
    return cadUser()

