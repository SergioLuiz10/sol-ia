from fastapi import FastAPI

from app.routers import chat, metricas, whatsapp

app = FastAPI(
    title="Assistente de WhatsApp - Distribuidora Sol",
    description="Atendimento automatizado de trocas, prazos de entrega e status de pedidos.",
    version="1.0.0",
)

app.include_router(chat.router)
app.include_router(metricas.router)
app.include_router(whatsapp.router)


# usado pelo servico de deploy para saber se a aplicacao esta no ar
@app.get("/health")
def health():
    return {"status": "ok"}
