#!/usr/bin/env bash
# testa o agente em producao com os cenarios do PRD
URL="https://sol-ia-production.up.railway.app"
TEL="71999990001"

perguntas=(
  "quanto tempo demora a entrega na pituba?" # prazo por bairro (bairro)
  "cade meu pedido 002?" # status do pedido (pedidos)
  "posso devolver um produto que nao gostei?" #política (RAG)
  "meu pedido 004 chega quando?" # status do pedido
  "voces dao desconto em compra grande?" # fora do escopo, tem que transferir
  "cade meu pedido 999?" # pedido que não existe, não pode inventar
)

for p in "${perguntas[@]}"; do
  echo "----------------------------------------"
  echo "> $p"
  curl -s -X POST "$URL/chat" \
    -H "Content-Type: application/json" \
    -d "{\"telefone\": \"$TEL\", \"mensagem\": \"$p\"}"
  echo
done

echo "----------------------------------------"
echo "> metricas"
curl -s "$URL/metricas"
echo
