import os
import random
import string
import configparser
from datetime import timedelta
from dotenv import load_dotenv


PASS_KEY = ''


load_dotenv(".env")


host = ""
db = ""
port = ""
user = ""
passwd = ""


DEBUG = True
SQLALCHEMY_DATABASE_URI =f"postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSONIFY_PRETTYPRINT_REGULAR = False
SECRET_KEY = "MLoD*jIHJay%TnT*6%3sdfs6El^j*Z^pn"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_TOKEN_LOCATION = ["headers", "cookies"]
JWT_REFRESH_COOKIE_PATH = '/Auth/Refresh'
JWT_COOKIE_SECURE = True # Em HTTPS deverá mudar para True

