from .Usuario import db, ma

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sigla = db.Column(db.String(6), nullable=False)
    nome = db.Column(db.String(150), nullable=False)

    def __init__(self, sigla, nome):
        self.sigla = sigla
        self.nome = nome

class ClienteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sigla', 'nome')


cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)
