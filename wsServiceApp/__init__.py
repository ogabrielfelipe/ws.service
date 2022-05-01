from pathlib import Path
import sqlite3
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
from .bluePrints.Relatorio import atendimentoRelatorio
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

app = Flask(__name__, template_folder= 'template', static_folder='static')
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
app.register_blueprint(atendimentoRelatorio.atendRel)


db.init_app(app)
ma.init_app(app)
jwt.init_app(app)
CORS(app)

from .bluePrints.Manager import manager



with app.app_context():

    #Cria usuário na base SQLite3
    camDataBase = str(Path('TABDEF.db').absolute())
    conn = sqlite3.connect(camDataBase)
    curs = conn.cursor()
    try:
        curs.execute("SELECT * from user")
    except:
        curs.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        );""")
        conn.commit()
        conn.close()

        conn3 = sqlite3.connect(camDataBase)
        curs = conn3.cursor()
        curs.execute("SELECT * from user")
    lu = curs.fetchone()  
    if lu is None:   
        conn4 = sqlite3.connect(camDataBase)
        curs = conn4.cursor()        
        curs2 = conn4.cursor()
        curs2.execute("INSERT INTO user (username, password) VALUES (?, ?)", ['wsService', generate_password_hash('@Acc0164')])
        conn4.commit()
        conn4.close()
    else:
        pass


    try:            
        #Cria as tabelas na base postgresql 
        db.create_all()

        try:
            extensao = db.session.execute(text("SELECT * FROM pg_available_extensions WHERE name = 'unaccent'")).one()
        except SQLAlchemyError as e:
            try:
                db.session.execute('CREATE EXTENSION UNACCENT;')
            except SQLAlchemyError as e:
                print(e)
            print(e)

        #Cria usuário na base Postgresql
        users_exist = Usuario.query.all()
        if not users_exist:
            user = Usuario('MASTER', 'Master', generate_password_hash('master1'), 0, 'master@master.com.br', 1)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
    except:
        pass