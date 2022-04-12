from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Enum
from .AcessoEnum import Acesso

db = SQLAlchemy()
ma = Marshmallow()


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(200))
    senha = db.Column(db.String, nullable=False)
    acesso = db.Column(Enum(Acesso), nullable=False)

    def __init__(self, username, nome, senha, acesso, email):
        self.username = username
        self.nome = nome
        self.senha = senha
        self.acesso = acesso
        self.email = email


class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'nome', 'email', 'acesso')


usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
