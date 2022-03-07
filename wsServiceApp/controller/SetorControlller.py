from sqlalchemy.exc import SQLAlchemyError
from ..model.Setor import Setor, setor_schema, setores_schema
from ..model.Usuario import db
from flask import request, jsonify


def cadastra_setor():
    resp = request.get_json()
    nome = resp['nome']
    cliente = resp['cliente']

    setor = Setor(nome=nome, cliente=cliente)

    try:
        db.session.add(setor)
        db.session.commit()
        result = setor_schema.dump(setor)
        return jsonify({'message': 'Setor com sucesso', 'dados': result}), 201
    except SQLAlchemyError as sa:
        print(sa)
        db.session.rollback()
        return jsonify({'message': 'Erro ao cadastrar', 'dados': {}}), 404


def atualiza_setor(id):
    resp = request.get_json()
    nome = resp['nome']
    cliente = resp['cliente']

    setor = Setor.query.get(id)
    if not setor:
        return jsonify({'message': 'Setor não encontrado', 'dados': {}}), 404

    try:
        setor.nome = nome
        setor.cliente = cliente
        db.session.commit()
        result = setor_schema.dump(setor)
        return jsonify({'message': 'Setor atualizado', 'dados': result}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}}), 500


def busca_setores():
    setor = Setor.query.all()
    if setor:
        result = setores_schema.dump(setor)
        return jsonify({'message': 'Sucesso', 'dados': result}), 200
    return jsonify({'message': 'Usuários não encontrado', 'dados': {}}), 404


def busca_setor(id):
    setor = Setor.query.get(id)
    if setor:
        result = setor_schema.dump(setor)
        return jsonify({'message': 'Sucesso', 'dados': result}), 200
    return jsonify({'message': 'Setor não encontrado', 'dados': {}}), 404


def delete_setor(id):
    setor = Setor.query.get(id)
    if not setor:
        return jsonify({'message': 'Setor não encontrado', 'dados': {}}), 404

    if setor:
        try:
            db.session.delete(setor)
            db.session.commit()
            result = setor_schema.dump(setor)
            return jsonify({'message': 'Setor excluido', 'dados': result}), 200
        except:
            return jsonify({'message': 'Não foi possível excluir', 'dados': {}}), 500
