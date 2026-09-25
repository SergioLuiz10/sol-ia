# Recebe telefone e mensagem do cliente, 
# processa usando o agente e registra a conversa.

from app.agent import agente
from app.repositories.conversas import registrar_conversa

# Função principal para responder mensagens de atendimento 
def responder(telefone: str, mensagem: str) -> str:
    resultado = agente.invoke(
        {
            "messages": [
                {
                    "role": "system",
                    "content": f"Telefone do cliente nesta conversa: {telefone}",
                },
                {"role": "user", "content": mensagem},
            ]
        }
    )

    mensagens = resultado["messages"]
    resposta = mensagens[-1].content

    # descobre qual tool o agente usou nesta conversa
    tool_usada = None
    for m in mensagens:
        nome = getattr(m, "name", None)
        if nome:
            tool_usada = nome

    transferiu = tool_usada == "transferir_para_humano"

    registrar_conversa( # registra a conversa no banco de dados
        telefone=telefone,
        pergunta=mensagem,
        resposta=resposta,
        tool_usada=tool_usada,
        transferiu=transferiu,
    )

    return resposta
