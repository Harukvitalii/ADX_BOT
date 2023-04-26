from dotenv import load_dotenv
import os
# Теперь используем вместо библиотеки python-dotenv библиотеку environs
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Забираем значение типа str
ADX_POSTER_TOKEN = os.getenv("ADX_POSTER_TOKEN")
ADX_POSTER_USERNAME =os.getenv("ADX_POSTER_USERNAME")
ADMIN = os.getenv("ADMIN")  # admin id
QIWI_BILL_DELL = 5 #minutes
QIWI_P2P_TOKEN = os.getenv('QIWI_P2P_TOKEN')
HOST = os.getenv('HOST')
user = os.getenv('user')
password = os.getenv('password')
db_name = os.getenv('db_name')
port = os.getenv('port')
"""IMGUR"""
CLIENT_ID = "8fcca220910c939" #FAKE
CLIENT_SECRET = 'dcaf0c3c1705f95111a8552e985f5212cc9a881f' #FAKE
