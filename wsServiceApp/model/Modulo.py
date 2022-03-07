from .Usuario import db, ma


class Modulo(db.Model):
    __tablename__ = 'modulo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sigla = db.Column(db.String(6))
    nome = db.Column(db.String(100), nullable=False)
    sistema = db.Column(db.Integer, db.ForeignKey('sistema.id'))

    def __init__(self, sigla, nome, sistema):
        self.sigla = sigla
        self.nome = nome
        self.sistema = sistema


class ModuloSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sigla', 'nome', 'sistema')


modulo_schema = ModuloSchema()
modulos_schema = ModuloSchema(many=True)
