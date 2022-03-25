from flask import Flask
from pydantic import conset
from .bluePrints.Login.auth import aut
from .model.Usuario import db, ma, Usuario
from .bluePrints.Login.auth import jwt
from sqlalchemy.event import listens_for
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
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


@listens_for(Engine, "connect")
def my_on_connect(dbapi_con, connection_record):
    if isinstance(dbapi_con, SQLite3Connection):
        cursor = dbapi_con.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


with app.app_context():
    db.create_all()
    users_exist = Usuario.query.all()
    if not users_exist:
        user = Usuario('master', 'Master', generate_password_hash('master1'), 0, 'master@master.com.br')
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)

