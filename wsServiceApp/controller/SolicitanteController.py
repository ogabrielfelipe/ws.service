from ..model.Usuario import db
from ..model.Solicitante import Solicitante, solicitante_schema, solicitantes_schema
from ..model.Setor import Setor
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from .util import convert_pesquisa_consulta
from sqlalchemy import text


def cadastra_solicitante():
    resp = request.get_json()
    nome = resp['nome']
    email = resp['email']
    setor = resp['setor']
    solicitante = Solicitante(nome=nome, email=email, setor=setor)
    try:
        db.session.add(solicitante)
        db.session.commit()
        result = solicitante_schema.dump(solicitante)
        return jsonify({'message': 'Cadastrado com sucesso', 'dados': result, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao cadastrar', 'dados': {}, 'error': str(e)}), 500


def atualiza_cadastro(id):
    resp = request.get_json()
    nome = resp['nome']
    email = resp['email']
    setor_id = resp['setor']

    solicitante = Solicitante.query.get(id)
    if not solicitante:
        return jsonify({'message': 'Solicitante não encontrado', 'dados': {}}), 404

    setor = Setor.query.get(setor_id)
    if not setor:
        return jsonify({'message': 'Setor não encontrado', 'dados': {}, 'error': ''}), 404


    try:
        solicitante.nome = nome
        solicitante.email = email
        solicitante.setor_id = setor
        db.session.commit()
        result = solicitante_schema.dump(solicitante)
        return jsonify({'message': 'Solicitante atualizado', 'dados': result, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}, 'error': str(e)}), 500


def busca_solicitantes():
    resp = request.get_json()    
    convert_dict_search = convert_pesquisa_consulta(resp)
    try:
        sql_solicitantes = text(f"""
        SELECT solicitante.id as id_solicitante, solicitante.nome as nome_solicitante, solicitante.email as email_solicitante,
            setor_id as setor_id, setor.nome as nome_setor, cliente_id as cliente_id, cliente.sigla as sigla_cliente,
            cliente.nome as nome_cliente FROM SOLICITANTE AS solicitante
        INNER JOIN SETOR as setor ON solicitante.setor_id = setor.id
        INNER JOIN CLIENTE as cliente ON setor.cliente_id = cliente.id
        {convert_dict_search}
        ORDER BY solicitante.id                
        """)
        consultaSolicitantes = db.session.execute(sql_solicitantes).fetchall()
        consultaSolicitantes_dict = [dict(u) for u in consultaSolicitantes]
        return jsonify({'msg': 'Busca efetuada com sucesso', 'dados': consultaSolicitantes_dict, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Nao foi efetuado a busca com sucesso', 'dados': {}, 'error': str(e)}), 500


def busca_solicitante(id):
    user = Solicitante.query.get(id)
    if user:
        result = solicitante_schema.dump(user)
        return jsonify({'message': 'Sucesso', 'dados': result, 'error': ''}), 200
    return jsonify({'message': 'Usuários não encontrado', 'dados': {}, 'error': ''}), 404


def delete_solicitante(id):
    solicitante = Solicitante.query.get(id)
    if not solicitante:
        return jsonify({'message': 'Solicitante não encontrado', 'dados': {}, 'error': ''}), 404

    if solicitante:
        try:
            db.session.delete(solicitante)
            db.session.commit()
            result = solicitante_schema.dump(solicitante)
            return jsonify({'message': 'Solicitante excluido', 'dados': result, 'error': ''}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Não foi possível exvluir', 'dados': {}, 'error': str(e)}), 500