# Canal de WhatsApp: recebe o webhook da Evolution API e responde pelo mesmo canal.
import os

import httpx
from fastapi import APIRouter, Request

from app.services.atendimento import responder

router = APIRouter()

EVOLUTION_URL = os.getenv("EVOLUTION_URL")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE")

# "5571...,5572..." vira ["5571...", "5572..."]
NUMEROS_PERMITIDOS = [
    numero.strip()
    for numero in (os.getenv("NUMEROS_PERMITIDOS") or "").split(",")
    if numero.strip()
]

# prefixo usado para testar mandando mensagem para si mesmo
PREFIXO_TESTE = "!teste "

# resposta padrao do webhook: ignorado e processado devolvem 200 do mesmo jeito,
# senao a Evolution reenvia a mesma mensagem varias vezes.
OK = {"ok": True}

# Função para enviar mensagens via WhatsApp usando a API do Evolution.
def enviar_whatsapp(numero: str, texto: str) -> None:
    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    httpx.post(
        url,
        headers={"apikey": EVOLUTION_API_KEY},
        json={"number": numero, "text": texto},
        timeout=30,
    )

# Função para extrair o texto de uma mensagem recebida via WhatsApp.
def extrair_texto(mensagem: dict) -> str | None:
    # mensagem simples
    texto = mensagem.get("conversation")
    if texto:
        return texto
    # mensagem com citacao ou formatacao
    return mensagem.get("extendedTextMessage", {}).get("text")

# Roteador para o endpoint de WhatsApp que recebe mensagens do webhook da Evolution API.
@router.post("/whatsapp")
async def whatsapp(requisicao: Request) -> dict:
    corpo = await requisicao.json()

    if corpo.get("event") != "messages.upsert":
        return OK

    dados = corpo.get("data") or {}
    chave = dados.get("key") or {}

    jid = chave.get("remoteJid") or ""
    if jid.endswith("@g.us"):  # grupo
        return OK

    telefone = jid.split("@")[0]
    if not telefone:
        return OK

    texto = extrair_texto(dados.get("message") or {})
    if not texto:  # audio, figurinha, foto
        return OK

    if chave.get("fromMe"):
        # teste no proprio chat: so responde com o prefixo, o que evita loop
        if not texto.startswith(PREFIXO_TESTE):
            return OK
        texto = texto[len(PREFIXO_TESTE) :]
    elif telefone not in NUMEROS_PERMITIDOS:
        return OK

    resposta = responder(telefone, texto)
    enviar_whatsapp(telefone, resposta)

    return OK
