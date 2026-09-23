
#pra pegar a conexão com o bd
from app.db import get_connection


#funcao q consulta para o agente o prazo de entrega para um determinado bairro
#usando conn para conectar cm o banco e cur para executar a consulta pegando o nome e o prazo de entrega do bairro
def consultar_prazo_bairro(bairro: str) -> str:
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT nome_bairro , prazo_dias FROM bairros WHERE nome_bairro ILIKE %s", ( bairro,))
        row = cur.fetchone()
        if row is None: 
            return f"Não encontrei o bairro '{bairro}' na nossa área de entrega."
        nome_bairro, prazo_dias = row
        return  f"Entregamos em {nome_bairro} em até {prazo_dias} dias úteis."
        
       