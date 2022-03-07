from sqlalchemy.exc import SQLAlchemyError
from ..model.Cliente import Cliente, cliente_schema, clientes_schema
from ..model.Usuario import db
from flask import request, jsonify


def cadastra_cliente():
    resp = request.get_json()
    sigla = resp['sigla']
    nome = resp['nome']

    cliente = Cliente(sigla=sigla, nome=nome)

    try:
        db.session.add(cliente)
        db.session.commit()
        result = cliente_schema.dump(cliente)
        return jsonify({'message': 'Cliente com sucesso', 'dados': result}), 201
    except SQLAlchemyError as sa:
        print(sa)
        db.session.rollback()
        return jsonify({'message': 'Erro ao cadastrar', 'dados': {}}), 404


def atualiza_cliente(id):
    resp = request.get_json()
    sigla = resp['sigla']
    nome = resp['nome']

    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'message': 'Cliente não encontrado', 'dados': {}}), 404

    try:
        cliente.nome = nome
        cliente.sigla = sigla
        db.session.commit()
        result = cliente_schema.dump(cliente)
        return jsonify({'message': 'Cliente atualizado', 'dados': result}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}}), 500


def busca_clientes():
    cliente = Cliente.query.all()
    if cliente:
        result = clientes_schema.dump(cliente)
        return jsonify({'message': 'Cliente', 'dados': result}), 200
    return jsonify({'message': 'Cliente não encontrado', 'dados': {}}), 404


def busca_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        result = cliente_schema.dump(cliente)
        return jsonify({'message': 'Sucesso', 'dados': result}), 200
    return jsonify({'message': 'Cliente não encontrado', 'dados': {}}), 404


def delete_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'message': 'Cliente não encontrado', 'dados': {}}), 404

    if cliente:
        try:
            db.session.delete(cliente)
            db.session.commit()
            result = cliente_schema.dump(cliente)
            return jsonify({'message': 'Cliente excluido', 'dados': result}), 200
        except:
            return jsonify({'message': 'Não foi possível excluir', 'dados': {}}), 500
