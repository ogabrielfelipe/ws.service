from flask import Flask
from pydantic import conset
from .bluePrints.Login.auth import aut
from .model.Usuario import db, ma, Usuario
from .bluePrints.Login.auth import jwt
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from wsServiceApp.bluePrints import (
    usuario,
    solicitante,
    sistema,
    setor,
    modulo,
    competencia,
    cliente,
    atendimento
)
from .model import (
    Solicitante,
    Sistema,
    Setor,
    Modulo,
    Competencia,
    Competencia,
    Cliente,
    Atendimento
)
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(aut)
app.register_blueprint(usuario.user)
app.register_blueprint(solicitante.soli)
app.register_blueprint(sistema.sist)
app.register_blueprint(setor.setor)
app.register_blueprint(modulo.mod)
app.register_blueprint(competencia.comp)
app.register_blueprint(cliente.client)
app.register_blueprint(atendimento.atend)


db.init_app(app)
ma.init_app(app)
jwt.init_app(app)
CORS(app)


with app.app_context():
    db.create_all()

    try:
        extensao = db.session.execute(text("SELECT * FROM pg_available_extensions WHERE name = 'unaccent'")).one()
    except SQLAlchemyError as e:
        try:
            db.session.execute('CREATE EXTENSION UNACCENT;')
        except SQLAlchemyError as e:
            print(e)
        print(e)

    users_exist = Usuario.query.all()
    if not users_exist:
        user = Usuario('master', 'Master', generate_password_hash('master1'), 0, 'master@master.com.br', 1)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)

