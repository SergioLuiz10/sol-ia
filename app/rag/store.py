from langchain_openai import OpenAIEmbeddings

import os 

from dotenv import load_dotenv

from langchain_postgres import PGVector

load_dotenv()

COLLECTION_NAME = "politica_trocas"
EMBEDDING_MODEL = "text-embedding-3-small"

CONNECTION_STRING  = os.getenv("DATABASE_URL_VECTOR")

if not CONNECTION_STRING:
    raise RuntimeError("DATABASE_URL_VECTOR não encontrada no .env")

# Função para obter a instância do PGVector
#retornando o objeto PGVector conectado ao bd com suporte a JSONB e modelo de embedding
def get_vectorstore() -> PGVector:
    return PGVector(
        embeddings=OpenAIEmbeddings(model=EMBEDDING_MODEL),
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True, 
    )


