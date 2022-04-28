from cryptography.fernet import Fernet
from wsServiceApp import app
from flask import Blueprint, redirect, render_template, request, url_for
from flask_jwt_extended import jwt_required


key = Fernet.generate_key()
fernet = Fernet(key)


@app.route('/Manager', methods=['GET', 'POST'])
def route_manager_login():
    if request.method == 'POST':
        if request.form['usuarioManager'] == 'wsServico' and request.form['senhaManager'] == '@Acc0164':            
            mensagem = 'usuarioautorizado'
            cipher = fernet.encrypt(mensagem.encode())
            return redirect(url_for('route_manager_painel', autorizacao = cipher))
        else:
            return render_template('index.html', msgUser = True)
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/Manager/Painel', methods=['GET', 'POST'])
def route_manager_painel():
    if request.method == 'GET':
        autorizacao = bytes(request.args['autorizacao'], 'utf8')
        print( autorizacao)
        autorizacao = fernet.decrypt(autorizacao).decode() 
        print(autorizacao)
        
        return render_template('painel.html')
    