from sqlalchemy.exc import SQLAlchemyError
from ..model.Competencia import Competencia, competencia_schema, competencias_schema
from ..model.Usuario import db
from ..model.Atendimento import Atendimento, atendimento_schema, atendimentos_schema
from ..controller.UsuarioController import usuario_username
from flask import request, jsonify
from datetime import datetime
from sqlalchemy import and_


def cadastra_competencia(usuario):
    resp = request.get_json()
    comp = resp['comp']
    ano = resp['ano']
    dataI = datetime.strptime(resp['dataI'], '%Y-%m-%d').date()
    dataF = datetime.strptime(resp['dataF'], '%Y-%m-%d').date()
    usuario = usuario_username(usuario).id
    trava = bool(resp['trava'])

    competencia = Competencia(comp=comp, ano=ano, dataI=dataI, dataF=dataF, trava=trava, usuario=usuario)
    if busca_competencia_por_usuario_comp_ano(comp=comp, ano=ano):
        try:
            db.session.add(competencia)
            db.session.commit()
            result = competencia_schema.dump(competencia)
            return jsonify({'message': 'Competencia com sucesso', 'dados': result}), 201
        except SQLAlchemyError as sa:
            print(sa)
            db.session.rollback()
            return jsonify({'message': 'Erro ao cadastrar', 'dados': {}}), 404
    else:
        return jsonify({'message': 'Já existe uma competencia criada', 'dados': {}}), 401

# Alteração de competencia, somente no intervalo entre datas
def atualiza_competencia(id):
    resp = request.get_json()
    dataI = datetime.strptime(resp['dataI'], '%Y-%m-%d').date()
    dataF = datetime.strptime(resp['dataF'], '%Y-%m-%d').date()

    competencia = Competencia.query.get(id)
    if not competencia:
        return jsonify({'message': 'Modulo não encontrado', 'dados': {}}), 404

    try:
        competencia.dataI = dataI
        competencia.dataF = dataF
        db.session.commit()
        result = competencia_schema.dump(competencia)
        return jsonify({'message': 'Competência atualizado', 'dados': result}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}}), 500


def altera_trava_competencia(id):
    resp = request.get_json()
    trava = bool(resp['trava'])

    competencia = Competencia.query.get(id)
    if not competencia:
        return jsonify({'message': 'Modulo não encontrado', 'dados': {}}), 404

    try:
        competencia.trava = trava
        db.session.commit()
        result = competencia_schema.dump(competencia)
        return jsonify({'message': 'Competência atualizado', 'dados': result}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}}), 500


def busca_competencias():
    competencia = Competencia.query.all()
    if competencia:
        result = competencias_schema.dump(competencia)
        return jsonify({'message': 'Competencia', 'dados': result}), 200
    return jsonify({'message': 'Competencia não encontrado', 'dados': {}}), 404


def busca_competencia(id):
    competencia = Competencia.query.get(id)
    if competencia:
        result = competencia_schema.dump(competencia)
        return jsonify({'message': 'Sucesso', 'dados': result}), 200
    return jsonify({'message': 'Competencia não encontrado', 'dados': {}}), 404


def busca_competencia_por_atendimento(id):
    competencia = Competencia.query.get(id)
    if competencia:
        return competencia_schema.dump(competencia)
    return None


def busca_competencia_por_usuario_comp_ano(comp, ano):
    competencia = Competencia.query.filter(and_(Competencia.comp == comp,
                                                Competencia.ano == ano))
    _comp = competencias_schema.dump(competencia)
    if not _comp:
        return True
    return False


# Somente deleta a competencia caso nao tenha atendimento vinculado a competencia
def delete_competencia(id):
    competencia = Competencia.query.get(id)
    if not competencia:
        return jsonify({'message': 'Competencia não encontrado', 'dados': {}}), 404

    if busca_atendimento_por_competencia(competencia.id):
        try:
            db.session.delete(competencia)
            db.session.commit()
            result = competencia_schema.dump(competencia)
            return jsonify({'message': 'Competencia excluido', 'dados': result}), 200
        except:
            return jsonify({'message': 'Não foi possível excluir', 'dados': {}}), 500
    else:
        return jsonify({'message': 'Competencia já possui Atendimento Vinculado', 'dados': {}}), 401


def busca_atendimento_por_competencia(idCompetencia):
    atendimento = Atendimento.query.filter(Atendimento.competencia == idCompetencia)
    _atendimento = atendimentos_schema.dump(atendimento)
    if _atendimento:
        return False
    return True