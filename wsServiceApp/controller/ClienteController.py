from sqlalchemy.exc import SQLAlchemyError
from ..model.Cliente import Cliente, cliente_schema, clientes_schema
from ..model.Usuario import db
from .util import convert_pesquisa_consulta
from flask import request, jsonify
from sqlalchemy import text


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
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'message': 'Erro ao cadastrar', 'dados': {}, 'error': str(e)}), 500


def atualiza_cliente(id):
    resp = request.get_json()
    sigla = resp['sigla']
    nome = resp['nome']

    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'message': 'Cliente não encontrado', 'dados': {}})

    try:
        cliente.nome = nome
        cliente.sigla = sigla
        db.session.commit()
        result = cliente_schema.dump(cliente)
        return jsonify({'message': 'Cliente atualizado', 'dados': result})
    except:
        db.session.rollback()
        return jsonify({'message': 'Não foi possível atualizar', 'dados': {}})


def busca_clientes():
    resp = request.get_json()
    print(resp)
    print(resp['id'][2])
    entry = {
        "id": int(resp['id'][2]),
        "nome": resp['nome'],
        "sigla": resp['sigla']
    }
    convert_dict_search = convert_pesquisa_consulta(entry)
    print('Consulta convertida: '+convert_dict_search)
    try:
        sql_clientes = text(f"SELECT * FROM CLIENTE {convert_dict_search}")
        consultaClientes = db.session.execute(sql_clientes).fetchall()
        consultaClientes_dict = [dict(u) for u in consultaClientes]
        return jsonify({'msg': 'Busca efetuada com sucesso', 'dados': consultaClientes_dict, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Nao foi efetuado a busca com sucesso', 'dados': {}, 'error': str(e)}), 500
    

def busca_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        result = cliente_schema.dump(cliente)
        return jsonify({'message': 'Sucesso', 'dados': result})
    return jsonify({'message': 'Cliente não encontrado', 'dados': {}})


def delete_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'message': 'Cliente não encontrado', 'dados': {}})

    if cliente:
        try:
            db.session.delete(cliente)
            db.session.commit()
            result = cliente_schema.dump(cliente)
            return jsonify({'message': 'Cliente excluido', 'dados': result})
        except:
            return jsonify({'message': 'Não foi possível excluir', 'dados': {}})
