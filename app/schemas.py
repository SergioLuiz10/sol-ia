from pydantic import BaseModel


# schema do que o usuário envia para o chat
class ChatRequest(BaseModel):
    mensagem: str 
    telefone: str



# schema do que o chat retorna para o usuário
class ChatResponse(BaseModel):
    resposta: str