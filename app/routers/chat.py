from fastapi import APIRouter

# Roteador para o endpoint de chat que recebe mensagens do cliente e responde usando o serviço de atendimento.
from app.schemas import ChatRequest, ChatResponse
from app.services.atendimento import responder

router = APIRouter()

# Endpoint para processar mensagens de chat.
# Recebe um objeto ChatRequest com o telefone e a mensagem do cliente. Retorna um ChatResponse com a resposta do atendimento.
@router.post("/chat", response_model=ChatResponse)
def chat(requisicao: ChatRequest) -> ChatResponse:
    resposta = responder(requisicao.telefone, requisicao.mensagem)
    return ChatResponse(resposta=resposta)
