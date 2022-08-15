from ..model.Competencia import Competencia, competencia_schema, competencias_schema
from ..model.Usuario import db
from ..model.Atendimento import Atendimento, atendimento_schema, atendimentos_schema
from ..controller.UsuarioController import usuario_username
from flask import request, jsonify
from datetime import datetime
from sqlalchemy import and_, text
from .util import calcula_intervalo_mes, convert_pesquisa_consulta


dict_english_portuguese = {
    "January": "Janeiro",
    "February": "Fevereiro",
    "March": "Março",
    "April": "Abril",
    "May": "Maio",
    "June": "Junho",
    "July": "Julho",
    "August": "Agosto",
    "September": "Setembro",
    "October": "Outubro",
    "November": "Novembro",
    "December": "Dezembro"
}


def cadastra_competencia(usuario):
    resp = request.get_json()
    comp = resp['comp']
    ano = resp['ano']
    intervalo_mes = calcula_intervalo_mes(str(comp)+'/'+str(ano))
    dataI = intervalo_mes[0]
    dataF = intervalo_mes[1]
    trava = bool(resp['trava'])

    competencia = Competencia(comp=comp, ano=ano, dataI=dataI, dataF=dataF, trava=trava, usuario=usuario['id'])
    if busca_competencia_por_usuario_comp_ano(comp=comp, ano=ano):
        if usuario['acesso'] == 0:                
            try:
                db.session.add(competencia)
                db.session.commit()
                result = competencia_schema.dump(competencia)
                return jsonify({'message': 'Competencia com sucesso', 'dados': result, 'error': ''}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': 'Erro ao cadastrar', 'dados': {}, 'error': str(e)}), 500
        else:
            return jsonify({'message': 'Usuario sem permissao', 'dados': {}, 'error': ''}), 401
    else:
        return jsonify({'message': 'Ja existe uma competencia criada', 'dados': {}, 'error': ''}), 401


def altera_trava_competencia(id, usuario):
    resp = request.get_json()
    trava = bool(resp['trava'])

    competencia = Competencia.query.get(id)
    if not competencia:
        return jsonify({'message': 'Competencia nao encontrado', 'dados': {}}), 404
    if usuario['acesso'] == 0:   
        try:
            competencia.trava = trava
            db.session.commit()
            result = competencia_schema.dump(competencia)
            return jsonify({'message': 'Competencia atualizado', 'dados': result}), 200
        except:
            db.session.rollback()
            return jsonify({'message': 'Nao foi possivel atualizar', 'dados': {}})
    else:
        return jsonify({'message': 'Usuario sem permissao', 'dados': {}, 'error': ''}), 401
    

def busca_competencias():
    resp = request.get_json()
    convert_dict_search = convert_pesquisa_consulta(resp)    
    try:
        sql_comp = text(f"""
                SELECT competencia.id as id_competencia, competencia.comp as mes_competencia, competencia.ano as ano_competencia,
                    to_char(competencia."dataI", 'DD/MM/YYYY') as data_inicial, to_char(competencia."dataF", 'DD/MM/YYYY') as data_final,
                    to_char(competencia."dataI", 'TMMonth/YYYY') as mes_ano_formatado, competencia.trava as trava_competencia, 
                    competencia.usuario_id as usuario_id, usuario.nome as nome_usuario
                FROM COMPETENCIA as competencia
                INNER JOIN USUARIO AS usuario on usuario.id = competencia.usuario_id
                {convert_dict_search}
                ORDER BY competencia.comp, competencia.ano
        """)
        consultaCompetencia = db.session.execute(sql_comp).fetchall()
        consultaCompetencia_dict = [dict(u) for u in consultaCompetencia]
        for x in range(0, len(consultaCompetencia_dict)):
            aux_consulta = consultaCompetencia_dict[x]['mes_ano_formatado'].split('/')
            aux_consulta[0] = dict_english_portuguese.get(aux_consulta[0])
            consultaCompetencia_dict[x]['mes_ano_formatado'] = '/'.join(aux_consulta)

        return jsonify({'msg': 'Busca efetuada com sucesso', 'dados': consultaCompetencia_dict, 'error': ''}), 200
    except Exception as e:
        return jsonify({'msg': 'Não foi possível fazer a busca', 'dados': {}, 'error': str(e)}), 500


def listar_competencias():
    currentDateTime = datetime.now()
    date = currentDateTime.date()
    ano = date.strftime("%Y")
    mes = date.strftime("%m")

    try:
        sql_comp = text(f'''SELECT competencia.id, competencia.comp, competencia.ano, 
                                competencia.trava 
                            FROM COMPETENCIA as competencia
                            WHERE competencia.comp = {int(mes)} AND competencia.ano = {int(ano)}
                            ''')
        consultaCompetencia = db.session.execute(sql_comp).fetchall()
        consultaCompetencia_dict = [dict(u) for u in consultaCompetencia]
        return jsonify({'msg': 'Busca efetuada com sucesso', 'dados': consultaCompetencia_dict, 'error': ''}), 200
    except Exception as e:
        return jsonify({'msg': 'Não foi possível fazer a busca', 'dados': {}, 'error': str(e)}), 500


def busca_competencia_por_atendimento(id):
    competencia = Competencia.query.get(id)
    if competencia:
        return competencia_schema.dump(competencia)
    return None


def busca_competencia_por_usuario_comp_ano(comp, ano):
    competencia = Competencia.query.filter(and_(Competencia.comp == comp,
                                                Competencia.ano == ano))
    _comp = competencias_schema.dump(competencia)
    if not _comp:
        return True
    return False


def delete_competencia(id, usuario):
    competencia = Competencia.query.get(id)
    if not competencia:
        return jsonify({'message': 'Competencia nao encontrado', 'dados': {}, 'error': ''}), 404

    if busca_atendimento_por_competencia(competencia.id):
        if usuario['acesso'] == 0:
            try:
                db.session.delete(competencia)
                db.session.commit()
                result = competencia_schema.dump(competencia)
                return jsonify({'message': 'Competencia excluido', 'dados': result, 'error': ''}), 200
            except Exception as e:
                return jsonify({'message': 'Nao foi possível excluir', 'dados': {}, 'error': str(e)}), 500
        else:
            return jsonify({'message': 'Usuario sem permissao', 'dados': {}, 'error': ''}), 401
    else:
        return jsonify({'message': 'Competencia ja possui Atendimento Vinculado', 'dados': {}, 'error': ''}), 403


def busca_atendimento_por_competencia(idCompetencia):
    atendimento = Atendimento.query.filter(Atendimento.competencia_id == idCompetencia)
    _atendimento = atendimentos_schema.dump(atendimento)
    if _atendimento:
        return False
    return True
    