from .Usuario import db, ma


class Competencia(db.Model):
    __tablename__ = 'competencia'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comp = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    dataI = db.Column(db.Date, nullable=False)
    dataF = db.Column(db.Date, nullable=False)
    trava = db.Column(db.Boolean, default=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    usuario = db.relationship('Usuario')

    def __init__(self, comp, ano, dataI, dataF, trava, usuario):
        self.comp = comp
        self.ano = ano
        self.dataI = dataI
        self.dataF = dataF
        self.trava = trava
        self.usuario_id = usuario


class CompetenciaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'comp', 'ano', 'dataI', 'dataF', 'trava', 'usuario_id')


competencia_schema = CompetenciaSchema()
competencias_schema = CompetenciaSchema(many=True)
