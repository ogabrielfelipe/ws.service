from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from ..model.Sistema import Sistema, sistema_schema, sistemas_schema
from ..model.Usuario import db
from .util import convert_pesquisa_consulta
from sqlalchemy import text


def cadastra_sistema():
    resp = request.get_json()
    sigla = resp['sigla']
    nome = resp['nome']

    sistema = Sistema(sigla=sigla, nome=nome)

    try:
        db.session.add(sistema)
        db.session.commit()
        result = sistema_schema.dump(sistema)
        return jsonify({'message': 'Sistema com sucesso', 'dados': result, 'error': ''}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao cadastrar', 'dados': {}, 'error': str(e)}), 500


def atualiza_sistema(id):
    resp = request.get_json()
    nome = resp['nome']
    sigla = resp['sigla']

    sistema = Sistema.query.get(id)
    if not sistema:
        return jsonify({'message': 'Sistema não encontrado', 'dados': {}, 'error': ''}), 404

    try:
        sistema.nome = nome
        sistema.sigla = sigla
        db.session.commit()
        result = sistema_schema.dump(sistema)
        return jsonify({'message': 'Solicitante atualizado', 'dados': result, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}, 'error': str(e)}), 500

def busca_sistemas():
    resp = request.get_json()    
    convert_dict_search = convert_pesquisa_consulta(resp)
    try:
        sql_sistemas = text(f"""
            SELECT * FROM SISTEMA
            {convert_dict_search}
            ORDER BY id
             """)
        consultaSistemas = db.session.execute(sql_sistemas).fetchall()
        consultaSistemas_dict = [dict(u) for u in consultaSistemas]
        return jsonify({'msg': 'Busca efetuada com sucesso', 'dados': consultaSistemas_dict, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Nao foi efetuado a busca com sucesso', 'dados': {}, 'error': str(e)}), 500


def busca_sistema(id):
    sistema = Sistema.query.get(id)
    if sistema:
        result = sistema_schema.dump(sistema)
        return jsonify({'message': 'Sucesso', 'dados': result, 'error': ''}), 200
    return jsonify({'message': 'Usuários não encontrado', 'dados': {}, 'error': ''}), 500


def delete_sistema(id):
    sistema = Sistema.query.get(id)
    if not sistema:
        return jsonify({'message': 'Sistema não encontrado', 'dados': {}}), 404

    if sistema:
        try:
            db.session.delete(sistema)
            db.session.commit()
            result = sistema_schema.dump(sistema)
            return jsonify({'message': 'Sistema excluido', 'dados': result, 'error': ''}), 200
        except Exception as e:
            return jsonify({'message': 'Não foi possível excluir', 'dados': {}, 'error': str(e)}), 500
