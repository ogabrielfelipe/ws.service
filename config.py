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
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSONIFY_PRETTYPRINT_REGULAR = False
SECRET_KEY = chave
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)
JWT_TOKEN_LOCATION = ["headers"]
JWT_COOKIE_SECURE = False # Em HTTPS deverá mudar para True

