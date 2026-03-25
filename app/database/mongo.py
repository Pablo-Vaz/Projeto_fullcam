from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

BANCO_MONGO = os.getenv('MONGO_URL')

conexao = MongoClient(BANCO_MONGO)

db = conexao['camera_db']
colecao = db['eventos']
    

def salvar(dados):

    try:
        colecao.insert_one(dados)
    except Exception as e:
        print('Erro ao salvar')
        raise e