from sqlalchemy.exc import SQLAlchemyError
from ..model.Setor import Setor, setor_schema, setores_schema
from ..model.Usuario import db
from flask import request, jsonify
from .util import convert_pesquisa_consulta
from sqlalchemy import text


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
        return jsonify({'message': 'Erro ao cadastrar', 'dados': {}}), 500


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
        return jsonify({'message': 'Setor atualizado', 'dados': result}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}}), 500


def busca_setores():
    resp = request.get_json()    
    convert_dict_search = convert_pesquisa_consulta(resp)
    try:
        sql_setores = text(f"""
            SELECT s.id as id_setor, s.nome as nome_setor, s.cliente_id, c.sigla as sigla_cliente, c.nome as nome_cliente FROM SETOR as s
            INNER JOIN cliente c on c.id = s.cliente_id
            {convert_dict_search}            
            ORDER BY s.id """)
        consultaSetores = db.session.execute(sql_setores).fetchall()
        consultaSetores_dict = [dict(u) for u in consultaSetores]
        return jsonify({'msg': 'Busca efetuada com sucesso', 'dados': consultaSetores_dict, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Nao foi efetuado a busca com sucesso', 'dados': {}, 'error': str(e)}), 500
        

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
