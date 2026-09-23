from app.db import get_connection


# Função para registrar uma conversa no sistema
def registrar_conversa(
    telefone: str,
    pergunta: str,
    resposta: str,
    tool_usada: str | None = None,
    transferiu: bool = False,
) -> None:
        with get_connection() as conn, conn.cursor() as cur:
             cur.execute(
            """
            INSERT INTO conversas (telefone, pergunta, resposta, tool_usada, transferiu)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (telefone, pergunta, resposta, tool_usada, transferiu),
        )

# Função para calcular a taxa de resolução das conversas.
# Retorna a taxa de resolução como um valor entre 0 e 1.
def calcular_taxa_resolucao() -> float:
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
          SELECT COUNT(*) AS total,
              COUNT(*) FILTER (WHERE transferiu = FALSE) AS resolvidas
          FROM conversas
            """
        )
        total, resolvidas = cur.fetchone()
        # Evita divisão por zero caso não haja conversas registradas.
        return resolvidas / total if total > 0 else 0.0