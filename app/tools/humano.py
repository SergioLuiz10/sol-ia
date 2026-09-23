from app.db import get_connection



#função para transferir um atendimento da IA para um humano
#passando o telefone do cliente e o motivo da transferência para registrar no bd
def transferir_humano(telefone: str , motivo: str) -> str:
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
        "INSERT INTO transferencias (telefone, motivo) VALUES (%s, %s)",
            (telefone, motivo),
        )
        return (
        "Vou te encaminhar para um atendente humano. "
        "Já registrei seu contato e em breve alguém fala com você."
    )