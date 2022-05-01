import json
from cairo import Path
from flask import jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
import configparser






def testa_conexao():
    resp = request.get_json()
    url = resp['url']
    username = resp['username']
    nomeDB = resp['nomeDB']
    porta = resp['porta']
    senha = resp['senha']

    try:
        con = psycopg2.connect(host= url, 
                         database=nomeDB,
                         port=porta,
                         user=username, 
                         password=senha)
        
        return jsonify({'msg': 'Conexao efetuada com sucesso', 'error': ''}), 200
    except SQLAlchemyError as se:
        return jsonify({'msg': 'Nao foi possivel fazer a conexao', 'error': str(se)}), 500


def salva_ini_conexao():
    resp = request.get_json()
    config = configparser.ConfigParser()
    config['DB'] = resp
    try:
        with open('CONFIG.ini', 'w', encoding='UTF-8') as confingfile:
            config.write(confingfile)
        return jsonify({'msg': 'Salvo com secesso'}), 200
    except Exception as e:
        return jsonify({'msg': 'Nao foi possivel gerar o arquivo', 'error': str(e)}), 500


def Buscar_ini_conexao():
    config = configparser.ConfigParser()
    try:
        config.read('CONFIG.ini')
        result = {
            'url': config['DB']['url'], 
            'nameDB': config['DB']['nomedb'], 
            'porta': config['DB']['porta'], 
            'username': config['DB']['username'] 
        }
        return jsonify({'msg': 'Busca efetuada com sucesso', 'dados': result}), 200
    except Exception as e:
        return jsonify({'msg': 'Nao foi possivel ler o arquivo ini', 'error': str(e)}), 500
    
