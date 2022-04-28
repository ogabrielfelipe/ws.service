from sqlalchemy.exc import SQLAlchemyError

from wsServiceApp.controller.util import convert_pesquisa_consulta
from ..model.Atendimento import Atendimento, atendimento_schema, atendimentos_schema
from .CompetenciaController import busca_competencia_por_atendimento
from ..model.Usuario import db
from ..controller.UsuarioController import usuario_username
from flask import request, jsonify
from sqlalchemy import and_, text
from datetime import datetime


def cadastra_atendimento(usuario):
    resp = request.get_json()
    
    try:
        data = datetime.strptime(resp['data'], '%Y-%m-%d').date()
    except Exception as e:
        return jsonify({'msg': 'Nao foi possivel converter a data de abertura', 'dados': '', 'error': str(e)}), 500
    
    demanda = resp['demanda']
        
    if not resp['dataE']:
        dataE = None
    else:
        try:
            dataE = datetime.strptime(resp['dataE'], '%Y-%m-%d').date()
        except Exception as e:
            return jsonify({'msg': 'Nao foi possivel converter a data de encerramento', 'dados': '', 'error': str(e)}), 500
    
    usuario = usuario['id']
    competencia = resp['competencia']
    solicitante = resp['solicitante']
    modulo = resp['modulo']
    desfecho = resp['desfecho']
    status = resp['status']
    observacao = resp['observacao']

    compTrava = busca_competencia_por_atendimento(competencia)
    if compTrava:
        if not bool(compTrava['trava']):
            if data >= datetime.strptime(compTrava['dataI'], '%Y-%m-%d').date() and data <= datetime.strptime(compTrava['dataF'], '%Y-%m-%d').date():
                atendimento = Atendimento(data=data, dataE=dataE, demanda=demanda, observacao=observacao, usuario=usuario, competencia=competencia,
                                    solicitante=solicitante, modulo=modulo, desfecho=desfecho, status=status)
                try:
                    db.session.add(atendimento)
                    db.session.commit()
                    result = atendimento_schema.dump(atendimento)
                    return jsonify({'msg': 'Atendimento cadastrado com sucesso', 'dados': result, 'error': ''}), 201
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'msg': 'Erro ao cadastrar', 'dados': {}, 'error': str(e)}), 500
            else:
                return jsonify({'msg': 'Data de cadastro nao compativel com a competencia', 'dados': {}, 'error': ''}), 403
        else:
            return jsonify({'msg': 'Competencia Finalizada', 'dados': {}, 'error': ''}), 403
    else:
        return jsonify({'msg': 'Competencia nao cadastrada', 'dados': {}, 'error': ''}), 404


def atualiza_atendimento(id):
    resp = request.get_json()
    data = datetime.strptime(resp['data'], '%Y-%m-%d').date() 
    demanda = resp['demanda']
    observacao = resp['observacao']
    try:
        dataE = datetime.strptime(resp['dataE'], '%Y-%m-%d').date() 
    except:
        dataE = None
    solicitante = resp['solicitante']
    modulo = resp['modulo']
    desfecho = resp['desfecho']
    status = resp['status']

    atendimento = Atendimento.query.get(id)

    compTrava = busca_competencia_por_atendimento(atendimento.competencia_id)
    if compTrava:
        if not bool(compTrava['trava']):
            if not atendimento:
                return jsonify({'msg': 'Atendimento não encontrado', 'dados': {}, 'error': ''}), 404

            if data >= datetime.strptime(compTrava['dataI'], '%Y-%m-%d').date() and data <= datetime.strptime(compTrava['dataF'], '%Y-%m-%d').date():
                try:
                    atendimento.data = data
                    atendimento.demanda = demanda
                    atendimento.dataencerra = dataE
                    atendimento.solicitante_id = solicitante
                    atendimento.modulo_id = modulo
                    atendimento.desfecho = desfecho
                    atendimento.status = status
                    atendimento.observacao = observacao
                    db.session.commit()
                    result = atendimento_schema.dump(atendimento)
                    return jsonify({'msg': 'Atendimento atualizado', 'dados': result, 'error': ''}), 200
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'msg': 'Não foi possível atualizar', 'dados': {}, 'error': str(e)}), 500
            else:
                return jsonify({'msg': 'Data de Abertura não pode ser maior ou menor do que a competencia', 'dados': {}, 'error': ''}), 403

        elif bool(compTrava['trava']):
            if not atendimento:
                return jsonify({'msg': 'Atendimento não encontrado', 'dados': {}, 'error': ''}), 404
            
            try:
                atendimento.observacao = observacao
                atendimento.desfecho = desfecho
                atendimento.status = status
                atendimento.dataencerra = dataE
                db.session.commit()
                result = atendimento_schema.dump(atendimento)
                return jsonify({'msg': 'Atendimento atualizado, somente os campos (desfecho, status, dataEncerramento)', 'dados': result, 'error': ''}), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'msg': 'Não foi possível atualizar os campos (desfecho, status, dataEncerramento)', 'dados': {}, 'error': str(e)}), 500
    else:
        return jsonify({'msg': 'Competencia nao cadastrada', 'dados': {}, 'error': ''}), 404


def busca_atendimentos_personalizada(usuario_id):    
    resp = request.get_json()    
    user_json = {
        'atendimento.usuario_id': ['AND', '=', usuario_id]
    }
    resp.update(user_json)
    convert_dict_search = convert_pesquisa_consulta(resp)
    try:
        sql_atendimentos = text(f"""
            SELECT atendimento.id as id_atendimento, to_char(atendimento.data, 'DD/MM/YYYY') as data_abertura,
                    to_char(atendimento.dataencerra, 'DD/MM/YYYY') as data_encerramento, competencia.id as competencia_id,
                    competencia.comp as competencia, competencia.ano as ano_competencia, atendimento.modulo_id as modulo_id,
                    modulo.sigla as sigla_modulo, modulo.nome as nome_modulo, modulo.sistema as sistema_id,
                    sistema.sigla as sigla_sistema, sistema.nome as nome_sistema, cliente.id as cliente_id, cliente.nome as nome_cliente,
                    cliente.sigla as sigla_cliente, solicitante.id as solicitante_id, solicitante.nome as nome_solicitante,
                    setor.id as setor_id, setor.nome as nome_setor, atendimento.demanda as demanda_atendimento,
                    atendimento.observacao as observacao_atendimento, atendimento.desfecho as desfecho_atendimento,
                    atendimento.status as status_atendimento, usuario.id as usuario_id, usuario.nome as nome_usuario
            FROM ATENDIMENTO AS atendimento
            INNER JOIN COMPETENCIA AS competencia ON competencia.id = atendimento.competencia_id
            INNER JOIN MODULO AS modulo ON modulo.id = atendimento.modulo_id
            INNER JOIN SISTEMA AS sistema ON sistema.id = modulo.sistema
            INNER JOIN SOLICITANTE AS solicitante ON solicitante.id = atendimento.solicitante_id
            INNER JOIN USUARIO AS usuario on usuario.id = atendimento.usuario_id
            INNER JOIN SETOR AS setor ON setor.id = solicitante.setor_id
            INNER JOIN CLIENTE AS cliente on cliente.id = setor.cliente_id
            {convert_dict_search}
        """)
        consultaAtendimentos = db.session.execute(sql_atendimentos).fetchall()
        consultaAtendimentos_dict = [dict(u) for u in consultaAtendimentos]

        sql_count_atendimentos = text(f"""
            SELECT atendimento.status as status_atendimento, count(atendimento.status) as total_atendimento 
                FROM ATENDIMENTO AS atendimento
            INNER JOIN COMPETENCIA AS competencia ON competencia.id = atendimento.competencia_id
            INNER JOIN MODULO AS modulo ON modulo.id = atendimento.modulo_id
            INNER JOIN SISTEMA AS sistema ON sistema.id = modulo.sistema
            INNER JOIN SOLICITANTE AS solicitante ON solicitante.id = atendimento.solicitante_id
            INNER JOIN USUARIO AS usuario on usuario.id = atendimento.usuario_id
            INNER JOIN SETOR AS setor ON setor.id = solicitante.setor_id
            INNER JOIN CLIENTE AS cliente on cliente.id = setor.cliente_id
            {convert_dict_search}
            GROUP BY atendimento.status
            HAVING atendimento.status IN ('ABERTO', 'ENCERRADO');
        """)
        consultaAtendimentosCount = db.session.execute(sql_count_atendimentos).fetchall()
        consultaAtendimentosCount_dict = [dict(u) for u in consultaAtendimentosCount]
        dados_count_atendimento = {}
        for x in consultaAtendimentosCount_dict:
           if x['status_atendimento'] == 'ABERTO':
                aux_dados1={
                            x['status_atendimento'] : x['total_atendimento']
                        }
                dados_count_atendimento.update(aux_dados1)
           elif x['status_atendimento'] == 'ENCERRADO':
                aux_dados2={
                            x['status_atendimento'] : x['total_atendimento']
                        }
                dados_count_atendimento.update(aux_dados2)
        print(dados_count_atendimento)
        return jsonify({'msg': 'Busca efetuada com sucesso', 'dados': { 'atendimentos':consultaAtendimentos_dict, 
                                                                        'count_atendimentos': dados_count_atendimento
                                                                        }, 'error': ''}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Nao foi efetuado a busca com sucesso', 'dados': {}, 'error': str(e)}), 500
    

def delete_atendimento(id):
    atendimento = Atendimento.query.get(id)
    if not atendimento:
        return jsonify({'msg': 'Atendimento não encontrado', 'dados': {}, 'error': ''}), 404

    compTrava = busca_competencia_por_atendimento(atendimento.competencia_id)
    if compTrava:
        if not bool(compTrava['trava']):
            if atendimento:
                try:
                    db.session.delete(atendimento)
                    db.session.commit()
                    result = atendimento_schema.dump(atendimento)
                    return jsonify({'msg': 'Atendimento excluido', 'dados': result, 'error': ''}), 200
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'msg': 'Nao foi possivel excluir', 'dados': {}, 'error': str(e)}), 500
        else:
            return jsonify({'msg': 'Competencia Fechada', 'dados': {}, 'error': ''}), 403
    else:
        return jsonify({'msg': 'Competencia nao encontrada', 'dados': {}, 'error': ''}), 404
