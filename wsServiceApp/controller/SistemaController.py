from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from ..model.Sistema import Sistema, sistema_schema, sistemas_schema
from ..model.Usuario import db


def cadastra_sistema():
    resp = request.get_json()
    sigla = resp['sigla']
    nome = resp['nome']

    sistema = Sistema(sigla=sigla, nome=nome)

    try:
        db.session.add(sistema)
        db.session.commit()
        result = sistema_schema.dump(sistema)
        return jsonify({'message': 'Sistema com sucesso', 'dados': result})
    except SQLAlchemyError as sa:
        print(sa)
        db.session.rollback()
        return jsonify({'message': 'Erro ao cadastrar', 'dados': {}})


def atualiza_sistema(id):
    resp = request.get_json()
    nome = resp['nome']
    sigla = resp['sigla']

    sistema = Sistema.query.get(id)
    if not sistema:
        return jsonify({'message': 'Sistema não encontrado', 'dados': {}})

    try:
        sistema.nome = nome
        sistema.sigla = sigla
        db.session.commit()
        result = sistema_schema.dump(sistema)
        return jsonify({'message': 'Solicitante atualizado', 'dados': result})
    except:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}})

def busca_sistemas():
    sistema = Sistema.query.all()
    if sistema:
        result = sistemas_schema.dump(sistema)
        return jsonify({'message': 'Sucesso', 'dados': result})
    return jsonify({'message': 'Usuários não encontrado', 'dados': {}})


def busca_sistema(id):
    sistema = Sistema.query.get(id)
    if sistema:
        result = sistema_schema.dump(sistema)
        return jsonify({'message': 'Sucesso', 'dados': result})
    return jsonify({'message': 'Usuários não encontrado', 'dados': {}})


def delete_sistema(id):
    sistema = Sistema.query.get(id)
    if not sistema:
        return jsonify({'message': 'Sistema não encontrado', 'dados': {}})

    if sistema:
        try:
            db.session.delete(sistema)
            db.session.commit()
            result = sistema_schema.dump(sistema)
            return jsonify({'message': 'Sistema excluido', 'dados': result})
        except:
            return jsonify({'message': 'Não foi possível excluir', 'dados': {}})
