from pathlib import Path
import sqlite3
from cryptography.fernet import Fernet
from wsServiceApp import app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Blueprint, redirect, render_template, request, url_for
from flask_jwt_extended import jwt_required
from ...model.TABDEF.User import User
from werkzeug.security import check_password_hash


key = Fernet.generate_key()
fernet = Fernet(key)


login_manager = LoginManager(app)
login_manager.login_view = "route_manager_login"

camDataBase = str(Path('TABDEF.db').absolute())

@login_manager.user_loader
def load_user(user_id):
   conn = sqlite3.connect(camDataBase)
   curs = conn.cursor()
   curs.execute("SELECT * from user where user_id = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2])


@app.route('/Manager', methods=['GET', 'POST'])
def route_manager_login():
    if request.method == 'POST':
        username = request.form['usuarioManager']
        senha = request.form['senhaManager']
        try:
            conn = sqlite3.connect(camDataBase)
            curs = conn.cursor()
            curs.execute("SELECT * FROM user where username = (?)", [username])
            user = list(curs.fetchone())
            Us = load_user(user[0])
            if Us.username == username and check_password_hash(Us.password, senha):
                login_user(Us)
                return redirect(url_for('route_manager_painel'))
            else:
                return render_template('index.html', msgUser = True)
        except Exception as e:
            print(e)
            return render_template('index.html', msgUser = True)    
        
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/Manager/Painel', methods=['GET', 'POST'])
@login_required
def route_manager_painel():      
        return render_template('painel.html')


@app.route('/Manager/Logout', methods=['GET'])
@login_required
def route_manager_logout():
    logout_user()
    return redirect(url_for('route_manager_login'))
    

@app.route('/Manager/Painel/Configuracao/BD', methods=['GET', 'POST'])
@login_required
def route_manager_configuracao_bd():  
        return render_template('settingDB.html')