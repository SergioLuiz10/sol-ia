#pega as variáveis de ambiente
import os 
#para conexão com o banco (pg)
import psycopg 

from dotenv import load_dotenv
load_dotenv()


#pega a URL do banco
DATABASE_URL = os.getenv("DATABASE_URL")

#funcao q retorna a conexao com o banco
def get_connection():
   if not DATABASE_URL:
       raise ValueError("DATABASE_URL não está definida nas variáveis de ambiente")
   return psycopg.connect(DATABASE_URL)
