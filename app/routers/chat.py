# Roteador para o endpoint de chat.
from fastapi import APIRouter

# schemas que validam o que entra e sai do endpoint de chat
from app.schemas import ChatRequest, ChatResponse

# agente que processa as mensagens de chat
from app.agent import agente

# funcao para registrar conversas no banco de dados
from app.repositories.conversas import registrar_conversa

router = APIRouter()


# Endpoint para processar mensagens de chat.
@router.post("/chat", response_model=ChatResponse)
def chat(requisicao: ChatRequest) -> ChatResponse:
    # Processa a mensagem de chat usando o agente.
    resultado = agente.invoke(
        {
            "messages": [
                {
                    "role": "system",
                    "content": f"Telefone do cliente nesta conversa: {requisicao.telefone}",
                },
                {"role": "user", "content": requisicao.mensagem},
            ]
        }
    )
    # Extrai as mensagens do resultado do agente.
    mensagens = resultado["messages"]
    resposta = mensagens[-1].content

    # descobre qual tool o agente usou nesta conversa
    tool_usada = None
    for m in mensagens:
        nome = getattr(m, "name", None)
        if nome:
            tool_usada = nome

    transferiu = tool_usada == "transferir_para_humano"

    # Registra a conversa no banco de dados.
    registrar_conversa(
        telefone=requisicao.telefone,
        pergunta=requisicao.mensagem,
        resposta=resposta,
        tool_usada=tool_usada,
        transferiu=transferiu,
    )
    # Retorna a resposta do chat para o cliente.
    return ChatResponse(resposta=resposta)
