from .Usuario import db, ma


class Sistema(db.Model):
    __tablename__ = 'sistema'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sigla = db.Column(db.String(10), nullable=False)
    nome = db.Column(db.String(150), nullable=False)

    def __init__(self, sigla, nome):
        self.sigla = sigla
        self.nome = nome


class SistemaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sigla', 'nome')


sistema_schema = SistemaSchema()
sistemas_schema = SistemaSchema(many=True)
