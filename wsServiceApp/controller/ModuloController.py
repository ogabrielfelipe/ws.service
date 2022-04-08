from sqlalchemy.exc import SQLAlchemyError
from ..model.Modulo import Modulo, modulo_schema, modulos_schema
from ..model.Usuario import db
from flask import request, jsonify
from .util import convert_pesquisa_consulta
from sqlalchemy import text



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
        return jsonify({'message': 'Modulo com sucesso', 'dados': result, 'error': ''}), 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'message': 'Erro ao cadastrar', 'dados': {}, 'error': str(e)}), 500


def atualiza_modulo(id):
    resp = request.get_json()
    nome = resp['nome']
    sigla = resp['sigla']
    sistema = resp['sistema']

    modulo = Modulo.query.get(id)
    if not modulo:
        return jsonify({'message': 'Modulo não encontrado', 'dados': {}, 'error': ''}), 404

    try:
        modulo.nome = nome
        modulo.sigla = sigla
        modulo.sistema = sistema
        db.session.commit()
        result = modulo_schema.dump(modulo)
        return jsonify({'message': 'Setor atualizado', 'dados': result, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}, 'error': str(e)}), 500


def busca_modulos():
    resp = request.get_json()    
    convert_dict_search = convert_pesquisa_consulta(resp)
    try:
        sql_modulos = text(f"""
            SELECT modulo.id as id_modulo, modulo.sigla as sigla_modulo, modulo.nome as nome_modulo, sistema.id as sistema_id,
                sistema.sigla as sigla_sistema, sistema.nome as nome_sistema FROM MODULO as modulo
            INNER JOIN SISTEMA as sistema ON modulo.sistema = sistema.id
            {convert_dict_search}
            ORDER BY modulo.id
             """)
        consultaModulos = db.session.execute(sql_modulos).fetchall()
        consultaModulos_dict = [dict(u) for u in consultaModulos]
        return jsonify({'msg': 'Busca efetuada com sucesso', 'dados': consultaModulos_dict, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Nao foi efetuado a busca com sucesso', 'dados': {}, 'error': str(e)}), 500


def busca_modulo(id):
    modulo = Modulo.query.get(id)
    if modulo:
        result = modulo_schema.dump(modulo)
        return jsonify({'message': 'Sucesso', 'dados': result, 'error': ''}), 200
    return jsonify({'message': 'Modulo não encontrado', 'dados': {}, 'error': ''}), 500


def delete_modulo(id):
    modulo = Modulo.query.get(id)
    if not modulo:
        return jsonify({'message': 'Setor não encontrado', 'dados': {}, 'error': ''}), 404

    if modulo:
        try:
            db.session.delete(modulo)
            db.session.commit()
            result = modulo_schema.dump(modulo)
            return jsonify({'message': 'Modulo excluido', 'dados': result, 'error': ''}), 200
        except:
            return jsonify({'message': 'Não foi possível excluir', 'dados': {}, 'error': ''}), 500
