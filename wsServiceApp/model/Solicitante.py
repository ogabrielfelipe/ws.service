from .Usuario import db, ma


class Solicitante(db.Model):
    __tablename__ = 'solicitante'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150))
    setor_id = db.Column(db.Integer, db.ForeignKey('setor.id'))
    setor = db.relationship('Setor', backref='solicitante')

    def __init__(self, nome, email, setor):
        self.nome = nome
        self.email = email
        self.setor_id = setor


class SolicitanteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nome', 'email', 'setor_id')


solicitante_schema = SolicitanteSchema()
solicitantes_schema = SolicitanteSchema(many=True)
