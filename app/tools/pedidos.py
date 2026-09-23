from app.db import get_connection


# funcao que consulta para o agente o status de um pedido pelo seu numero
def consultar_status_pedido(numero_pedido: str) -> str:
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT p.numero_pedido, p.cliente, p.status, p.data_prevista, b.nome_bairro
            FROM pedidos p
            JOIN bairros b ON p.bairro_id = b.id
            WHERE p.numero_pedido ILIKE %s
            """,
            (numero_pedido,),
        )
        row = cur.fetchone()

        if row is None:
            return (
                f"Não encontrei nenhum pedido com o número '{numero_pedido}'. "
                "Pode conferir o número e me mandar de novo?"
            )

        numero, cliente, status, data_prevista, nome_bairro = row

        if status == "cancelado":
            return f"O pedido {numero}, de {cliente}, está cancelado."

        if data_prevista is None:
            return f"O pedido {numero}, de {cliente}, está com status '{status}' e ainda não tem data prevista de entrega."

        data = data_prevista.strftime("%d/%m/%Y")

        if status == "entregue":
            return f"O pedido {numero}, de {cliente}, foi entregue em {nome_bairro} no dia {data}."

        if status == "em transporte":
            return f"O pedido {numero}, de {cliente}, já saiu para entrega e chega em {nome_bairro} até {data}."

        return f"O pedido {numero}, de {cliente}, está sendo separado e a previsão de entrega em {nome_bairro} é {data}."
