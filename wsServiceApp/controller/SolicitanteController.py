from ..model.Usuario import db
from ..model.Solicitante import Solicitante, solicitante_schema, solicitantes_schema
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError


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
        return jsonify({'message': 'Cadastrado com sucesso', 'dados': result})
    except SQLAlchemyError as sa:
        print(sa)
        db.session.rollback()
        return jsonify({'message': 'Erro ao cadastrar', 'dados': {}})


def atualiza_cadastro(id):
    resp = request.get_json()
    nome = resp['nome']
    email = resp['email']
    setor = resp['setor']

    solicitante = Solicitante.query.get(id)
    if not solicitante:
        return jsonify({'message': 'Solicitante não encontrado', 'dados': {}})

    try:
        solicitante.nome = nome
        solicitante.email = email
        solicitante.setor_id = setor
        db.session.commit()
        result = solicitante_schema.dump(solicitante)
        return jsonify({'message': 'Solicitante atualizado', 'dados': result})
    except:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}})


def busca_solicitantes():
    users = Solicitante.query.all()
    if users:
        result = solicitantes_schema.dump(users)
        return jsonify({'message': 'Sucesso', 'dados': result})
    return jsonify({'message': 'Usuários não encontrado', 'dados': {}})


def busca_solicitante(id):
    user = Solicitante.query.get(id)
    if user:
        result = solicitante_schema.dump(user)
        return jsonify({'message': 'Sucesso', 'dados': result})
    return jsonify({'message': 'Usuários não encontrado', 'dados': {}})


def delete_solicitante(id):
    solicitante = Solicitante.query.get(id)
    if not solicitante:
        return jsonify({'message': 'Solicitante não encontrado', 'dados': {}})

    if solicitante:
        try:
            db.session.delete(solicitante)
            db.session.commit()
            result = solicitante_schema.dump(solicitante)
            return jsonify({'message': 'Solicitante excluido', 'dados': result})
        except:
            return jsonify({'message': 'Não foi possível exvluir', 'dados': {}})