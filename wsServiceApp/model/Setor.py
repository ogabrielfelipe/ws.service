from .Usuario import db, ma


class Setor(db.Model):
    __tablename__ = 'setor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cliente = db.relationship('Cliente')

    def __init__(self, nome, cliente):
        self.nome = nome
        self.cliente_id = cliente


class SetorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome', 'cliente_id')


setor_schema = SetorSchema()
setores_schema = SetorSchema(many=True)
