# sol-ia

Assistente de WhatsApp para a Distribuidora Sol. Responde sobre política de trocas, prazo de entrega por bairro e status de pedido, e transfere para um atendente quando não sabe.

No ar em: https://sol-ia-production.up.railway.app/docs

O canal de WhatsApp esta ligado via Evolution API: mensagem recebida cai no webhook `/whatsapp`, passa pelo mesmo agente do `/chat` e a resposta volta pelo WhatsApp.

## Stack

FastAPI · LangChain · OpenAI (gpt-4o-mini) · Postgres + PGVector · Docker · Railway

## Como rodar

```bash
cp .env.example .env          # preencha OPENAI_API_KEY
docker compose up -d
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < data/schema.sql
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < data/seed.sql
python -m app.rag.ingest      # indexa a política no PGVector
```

A API sobe em http://localhost:8000/docs

## Como está organizado

```
app/
├── agent/          agente e as 4 tools expostas ao modelo
├── tools/          o que cada tool faz de verdade (SQL e RAG)
├── rag/            ingestão da política e configuração do PGVector
├── repositories/   acesso à tabela de conversas
├── services/       regra de atendimento, independente do canal
├── routers/        /chat, /whatsapp, /metricas, /health
└── schemas.py      contrato de entrada e saída da API
data/               schema, dados fictícios e política de trocas
prompt/sistema.md   regras do agente
```

## Decisões

**SQL para prazo e pedido, RAG para a política.** Prazo e status são dado exato que vive em tabela: uma busca por semelhança pode trazer a linha errada. A política é texto corrido, e aí a busca semântica funciona — o cliente escreve "não gostei" e acha a seção de arrependimento.

**O modelo não sabe nada sozinho.** Todo número, data ou regra vem do retorno de uma tool. O prompt proíbe estimar ou aproximar, e cada tool tem uma resposta pronta para o caso de não encontrar. É assim que o R5 é garantido.

**Transferência registrada, não só anunciada.** A tool grava telefone e motivo na tabela `transferencias`. O motivo é escrito pelo modelo, o que dá visibilidade do que mais cai para humano e do que vale automatizar depois.

**Toda conversa é logada** com a tool usada e se houve transferência. É o que alimenta a meta de 60% do PRD, em `/metricas`, e o que permite descobrir por que o agente errou quando ele errar.

**O canal não conhece a regra.** `/chat` e `/whatsapp` são só porta de entrada: os dois chamam a mesma função em `services/atendimento.py`, que fala com o agente e grava a conversa. O agente não sabe por onde a mensagem chegou, e trocar de provedor de WhatsApp mexe em um arquivo só.

**Evolution API em vez da API oficial.** A API oficial da Meta exige conta Business verificada, o que não fecha no prazo de um teste. A Evolution roda como serviço próprio e expõe a mesma ideia: webhook na entrada, POST na saída.

**Lista de números permitidos.** O número pareado é pessoal, então o webhook só responde quem está em `NUMEROS_PERMITIDOS`. Grupos, áudios e figurinhas são ignorados. Fica em variável de ambiente para mudar sem deploy.

**Railway em vez de VPS.** HTTPS pronto (o webhook do WhatsApp exige) e deploy a cada push. Para um cliente real, avaliaria VPS ou cloud pelo custo e pelo controle.

**Dados fictícios.** Bairros e prazos de Salvador, pedidos cobrindo os quatro status. Combinado com o Vinicius antes de começar.

## Métrica

`GET /metricas` devolve a taxa de conversas resolvidas sem transferência, a meta e se ela foi atingida.

Transferir não é erro: é o comportamento certo quando o dado não existe. A taxa mede quanto atendimento saiu do time, não se a resposta está correta.

## Limitações e próximos passos

- A busca por bairro ignora maiúscula, mas não acento: "Federacao" não encontra "Federação". Resolveria com a extensão `unaccent`.
- Sem memória entre mensagens: cada mensagem é tratada isolada.
- A transferência para na tabela. O próximo passo é avisar o atendente no WhatsApp.
- O WhatsApp está num número pessoal com lista de permitidos, o que serve para demonstrar. Em produção seria um número dedicado e a API oficial.
- Sem testes automatizados. Para medir corretude, montaria um conjunto de perguntas com resposta esperada e rodaria a cada mudança no prompt.
- O aviso de horário comercial ficou de fora desta versão.

## Testando

```bash
./testar_producao.sh
```

Cobre os seis cenários: prazo, pedido em transporte, política, pedido cancelado, assunto fora do escopo e pedido inexistente.
