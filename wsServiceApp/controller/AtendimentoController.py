from sqlalchemy.exc import SQLAlchemyError
from ..model.Atendimento import Atendimento, atendimento_schema, atendimentos_schema
from .CompetenciaController import busca_competencia_por_atendimento
from ..model.Usuario import db
from ..controller.UsuarioController import usuario_username
from flask import request, jsonify
from sqlalchemy import and_
from datetime import datetime


def cadastra_atendimento(usuario):
    resp = request.get_json()
    
    try:
        data = datetime.strptime(resp['data'], '%Y-%m-%d').date()
    except Exception as e:
        return jsonify({'msg': 'Nao foi possivel converter a data de abertura', 'dados': '', 'error': str(e)}), 500
    
    demanda = resp['demanda']
        
    if not resp['dataE']:
        dataE = ''
    else:
        try:
            dataE = datetime.strptime(resp['dataE'], '%Y-%m-%d').date()
        except Exception as e:
            return jsonify({'msg': 'Nao foi possivel converter a data de encerramento', 'dados': '', 'error': str(e)}), 500
    
    usuario = usuario['id']
    competencia = resp['competencia']
    solicitante = resp['solicitante']
    modulo = resp['modulo']
    desfecho = resp['desfecho']
    status = resp['status']

    compTrava = busca_competencia_por_atendimento(competencia)
    if compTrava['trava']:
        if data >= compTrava['dataF'] or data <= compTrava['dataI']:
            atendimento = Atendimento(data=data, dataE=dataE, demanda=demanda, usuario=usuario, competencia=competencia,
                                  solicitante=solicitante, modulo=modulo, desfecho=desfecho, status=status)
            try:
                db.session.add(atendimento)
                db.session.commit()
                result = atendimento_schema(atendimento)
                return jsonify({'message': 'Atendimento com sucesso', 'dados': result})
            except SQLAlchemyError as sa:
                print(sa)
                db.session.rollback()
                return jsonify({'message': 'Erro ao cadastrar', 'dados': {}})
        else:
            return jsonify({'message': 'Data de cadastro não compatível com a competência', 'dados': {}})
    else:
        return jsonify({'message': 'Competência Finalizada', 'dados': {}})



def atualiza_atendimento(id):
    resp = request.get_json()
    data = resp['data']
    demanda = resp['demanda']
    dataE = resp['dataE']
    solicitante = resp['solicitante']
    modulo = resp['modulo']
    desfecho = resp['desfecho']
    status = resp['status']

    atendimento = Atendimento.query.get(id)

    compTrava = busca_competencia_por_atendimento(atendimento.competencia_id)
    if compTrava['trava']:
        if not atendimento:
            return jsonify({'message': 'Atendimento não encontrado', 'dados': {}})
        try:
            atendimento.data = data
            atendimento.demanda = demanda
            atendimento.dataE = dataE
            atendimento.solicitante = solicitante
            atendimento.modulo = modulo
            atendimento.desfecho = desfecho
            atendimento.status = status
            db.session.commit()
            result = atendimento_schema.dump(atendimento)
            return jsonify({'message': 'Atendimento atualizado', 'dados': result})
        except:
            db.session.rollback()
            return jsonify({'message': 'Não foi possível atualizar', 'dados': {}})
    else:
        return jsonify({'message': 'Competencia Fechada', 'dados': {}})


def busca_atendimentos():
    resp = request.get_json()
    usuario = resp['usuario']
    competencia = resp['competencia']

    atendimento = Atendimento.query.filter(and_(Atendimento.usuario_id == usuario,
                                                Atendimento.competencia_id == competencia))
    if atendimento:
        result = atendimentos_schema.dump(atendimento)
        return jsonify({'message': 'Sucesso', 'dados': result}), 200
    return jsonify({'message': 'Atendimentos não encontrado', 'dados': {}})


def busca_atendimento(id):
    atendimento = Atendimento.query.get(id)
    if atendimento:
        result = atendimento_schema.dump(atendimento)
        return jsonify({'message': 'Sucesso', 'dados': result})
    return jsonify({'message': 'Atendimento não encontrado', 'dados': {}})


def delete_atendimento(id):
    atendimento = Atendimento.query.get(id)
    if not atendimento:
        return jsonify({'message': 'Atendimento não encontrado', 'dados': {}})

    compTrava = busca_competencia_por_atendimento(atendimento.competencia_id)
    if compTrava['trava']:
        if atendimento:
            try:
                db.session.delete(atendimento)
                db.session.commit()
                result = atendimento_schema.dump(atendimento)
                return jsonify({'message': 'Atendimento excluido', 'dados': result})
            except:
                return jsonify({'message': 'Não foi possível excluir', 'dados': {}})
    else:
        return jsonify({'message': 'Competência Fechada', 'dados': {}})

