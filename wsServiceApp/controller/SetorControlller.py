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
        return jsonify({'message': 'Setor com sucesso', 'dados': result})
    except SQLAlchemyError as sa:
        print(sa)
        db.session.rollback()
        return jsonify({'message': 'Erro ao cadastrar', 'dados': {}})


def atualiza_setor(id):
    resp = request.get_json()
    nome = resp['nome']
    cliente = resp['cliente']

    setor = Setor.query.get(id)
    if not setor:
        return jsonify({'message': 'Setor não encontrado', 'dados': {}})

    try:
        setor.nome = nome
        setor.cliente = cliente
        db.session.commit()
        result = setor_schema.dump(setor)
        return jsonify({'message': 'Setor atualizado', 'dados': result})
    except:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}})


def busca_setores():
    setor = Setor.query.all()
    if setor:
        result = setores_schema.dump(setor)
        return jsonify({'message': 'Sucesso', 'dados': result})
    return jsonify({'message': 'Usuários não encontrado', 'dados': {}})


def busca_setor(id):
    setor = Setor.query.get(id)
    if setor:
        result = setor_schema.dump(setor)
        return jsonify({'message': 'Sucesso', 'dados': result})
    return jsonify({'message': 'Setor não encontrado', 'dados': {}})


def delete_setor(id):
    setor = Setor.query.get(id)
    if not setor:
        return jsonify({'message': 'Setor não encontrado', 'dados': {}})

    if setor:
        try:
            db.session.delete(setor)
            db.session.commit()
            result = setor_schema.dump(setor)
            return jsonify({'message': 'Setor excluido', 'dados': result})
        except:
            return jsonify({'message': 'Não foi possível excluir', 'dados': {}})
