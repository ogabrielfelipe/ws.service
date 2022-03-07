from .Usuario import db, ma
from .DesfechoEnum import Desfecho
from .StatusEnum import Status
from sqlalchemy import Enum


class Atendimento(db.Model):
    __tablename__ = 'atendimento'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.Date, nullable=False)
    demanda = db.Column(db.String(1024), nullable=False)
    dataE = db.Column(db.Date)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario')
    competencia_id = db.Column(db.Integer, db.ForeignKey('competencia.id'), nullable=False)
    competencia = db.relationship('Competencia')
    solicitante_id = db.Column(db.Integer, db.ForeignKey('solicitante.id'), nullable=False)
    solicitante = db.relationship('Solicitante')
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)
    modulo = db.relationship('Modulo')
    desfecho = db.Column(Enum(Desfecho), nullable=False)
    status = db.Column(Enum(Status), nullable=False)

    def __init__(self, data, demanda, dataE, usuario, competencia, solicitante, modulo, desfecho, status):
        self.data = data
        self.demanda = demanda
        self.dataE = dataE
        self.usuario_id = usuario
        self.competencia_id = competencia
        self.solicitante_id = solicitante
        self.modulo_id = modulo
        self.desfecho = desfecho
        self.status = status


class AtendimentoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'data', 'demanda', 'dataE', 'usuario_id', 'competencia_id', 'solicitante_id', 'modulo_id',
                  'desfecho', 'status')


atendimento_schema = AtendimentoSchema()
atendimentos_schema = AtendimentoSchema(many=True)
