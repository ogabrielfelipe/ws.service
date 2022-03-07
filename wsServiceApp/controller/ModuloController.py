from sqlalchemy.exc import SQLAlchemyError
from ..model.Modulo import Modulo, modulo_schema, modulos_schema
from ..model.Usuario import db
from flask import request, jsonify


def cadastra_modulo():
    resp = request.get_json()
    nome = resp['nome']
    sigla = resp['sigla']
    sistema = resp['sistema']

    modulo = Modulo(nome=nome, sigla=sigla, sistema=sistema)

    try:
        db.session.add(modulo)
        db.session.commit()
        result = modulo_schema.dump(modulo)
        return jsonify({'message': 'Modulo com sucesso', 'dados': result}), 201
    except SQLAlchemyError as sa:
        print(sa)
        db.session.rollback()
        return jsonify({'message': 'Erro ao cadastrar', 'dados': {}}), 404


def atualiza_modulo(id):
    resp = request.get_json()
    nome = resp['nome']
    sigla = resp['sigla']
    sistema = resp['sistema']

    modulo = Modulo.query.get(id)
    if not modulo:
        return jsonify({'message': 'Modulo não encontrado', 'dados': {}}), 404

    try:
        modulo.nome = nome
        modulo.sigla = sigla
        db.session.commit()
        result = modulo_schema.dump(modulo)
        return jsonify({'message': 'Setor atualizado', 'dados': result}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}}), 500


def busca_modulos():
    modulo = Modulo.query.all()
    if modulo:
        result = modulos_schema.dump(modulo)
        return jsonify({'message': 'Modulo', 'dados': result}), 200
    return jsonify({'message': 'Modulo não encontrado', 'dados': {}}), 404


def busca_modulo(id):
    modulo = Modulo.query.get(id)
    if modulo:
        result = modulo_schema.dump(modulo)
        return jsonify({'message': 'Sucesso', 'dados': result}), 200
    return jsonify({'message': 'Modulo não encontrado', 'dados': {}}), 404


def delete_setor(id):
    modulo = Modulo.query.get(id)
    if not modulo:
        return jsonify({'message': 'Setor não encontrado', 'dados': {}}), 404

    if modulo:
        try:
            db.session.delete(modulo)
            db.session.commit()
            result = modulo_schema.dump(modulo)
            return jsonify({'message': 'Modulo excluido', 'dados': result}), 200
        except:
            return jsonify({'message': 'Não foi possível excluir', 'dados': {}}), 500
