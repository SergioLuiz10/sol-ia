#!/usr/bin/env bash
# testa o agente em producao com os cenarios do PRD
URL="https://sol-ia-production.up.railway.app"
TEL="71999990001"

perguntas=(
  "quanto tempo demora a entrega na pituba?"
  "cade meu pedido 002?"
  "posso devolver um produto que nao gostei?"
  "meu pedido 004 chega quando?"
  "voces dao desconto em compra grande?"
  "cade meu pedido 999?"
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
