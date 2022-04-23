import os
import time 
import datetime
from flask import request, jsonify, send_from_directory
from ...model.Usuario import db
from sqlalchemy import text
from ..util import convert_pesquisa_consulta
import pandas as pd
from pathlib import Path


tempPath = str(Path('temp/').absolute())


def relatorio_atendimento_ordem_data(usuario_logado):
    resp = request.get_json()
    convert_dict_search = convert_pesquisa_consulta(resp)
    try:
        sql_atendimentos = text(f"""
            SELECT atendimento.id as id_atendimetno, to_char(atendimento.data, 'DD/MM/YYYY') as data_abertura,
                to_char(atendimento.dataencerra, 'DD/MM/YYYY') as data_encerramento,
                competencia.comp as competencia, competencia.ano as ano_competencia,
                modulo.sigla as sigla_modulo, sistema.sigla as sigla_sistema, solicitante.nome as nome_solicitante,
                atendimento.demanda as demanda_atendimento,
                atendimento.observacao as observacao_atendimento, atendimento.desfecho as desfecho_atendimento,
                atendimento.status as status_atendimento, usuario.nome as nome_usuario
            FROM ATENDIMENTO AS atendimento
            INNER JOIN COMPETENCIA AS competencia ON competencia.id = atendimento.competencia_id
            INNER JOIN MODULO AS modulo ON modulo.id = atendimento.modulo_id
            INNER JOIN SISTEMA AS sistema ON sistema.id = modulo.sistema
            INNER JOIN SOLICITANTE AS solicitante ON solicitante.id = atendimento.solicitante_id
            INNER JOIN USUARIO AS usuario on usuario.id = atendimento.usuario_id            
            {convert_dict_search}
            ORDER BY atendimento.data
        """)
        consultaAtendimentos = db.session.execute(sql_atendimentos).fetchall()
        consultaAtendimentos_dict = [dict(u) for u in consultaAtendimentos]

        data = consultaAtendimentos_dict
        df = pd.DataFrame(data)
        verifica_diretorio_temp()
        varre_pasta_temp()
        nomeArquivoGerado = str(datetime.datetime.now())+'.xlsx'
        df.to_excel(tempPath+'/'+nomeArquivoGerado, index=False, header=True)
        return send_from_directory(tempPath, nomeArquivoGerado, as_attachment=True), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': 'Nao foi efetuado a busca com sucesso', 'dados': {}, 'error': str(e)}), 500
    

def varre_pasta_temp():
    lista_arquivos = []
    for diretorio, subpastas, arquivos in os.walk(tempPath):
        for arquivo in arquivos:
           lista_arquivos.append(os.path.join(diretorio, arquivo))

    data_atual = datetime.datetime.now().strftime("%d-%m-%Y")
    try:
        for x in lista_arquivos:
            ti_m = os.path.getmtime(x)   
            m_ti = time.ctime(ti_m) 
            t_obj = time.strptime(m_ti) 
            data_criacao_arquivo = time.strftime("%d-%m-%Y", t_obj)
            if datetime.datetime.strptime(data_criacao_arquivo, '%d-%m-%Y').date() != datetime.datetime.strptime(data_atual, '%d-%m-%Y').date():
                os.remove(x)
        return True
    except Exception as e:
        print(e)
        return False

def verifica_diretorio_temp():
    if os.path.isdir(tempPath):
        return True
    else:
        os.makedirs(tempPath)