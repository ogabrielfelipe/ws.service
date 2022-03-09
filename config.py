import os
import random
import string
import configparser
from datetime import timedelta
from dotenv import load_dotenv


config = configparser.ConfigParser()
config.read('CONFIGDB.ini')

load_dotenv(".env")

stringKey = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase
chave = ''.join(random.choice(stringKey) for i in range(12))

host = "db.bnrldhgbsuswrprchcij.supabase.co"
db = "postgres"
port = "5432"
user = "postgres"
passwd = "wIszTw5!&#9Z"

DEBUG = True
#SQLALCHEMY_DATABASE_URI = f"sqlite:///{config.get('DATABASE', 'DB')}"
SQLALCHEMY_DATABASE_URI =f"postgresql+psycopg2://ylwcvdoqhepgzk:ed14a8f362a6432a464b330282b1d670ecdf667c5f0f0fa2d359f635635a34c7@ec2-3-216-221-31.compute-1.amazonaws.com:5432/d27i67urteslmd"
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSONIFY_PRETTYPRINT_REGULAR = False
SECRET_KEY = chave
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)
JWT_TOKEN_LOCATION = ["headers"]
JWT_COOKIE_SECURE = False # Em HTTPS deverá mudar para True

