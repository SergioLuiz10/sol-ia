CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS bairros (
    id SERIAL PRIMARY KEY,
    nome_bairro VARCHAR(255) NOT NULL UNIQUE,
    prazo_dias INT NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos (
    id SERIAL PRIMARY KEY,
    numero_pedido VARCHAR(255) NOT NULL UNIQUE,
    cliente VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    bairro_id INT NOT NULL REFERENCES bairros(id),
    status text CHECK (status IN ('separando', 'em transporte', 'entregue', 'cancelado')) NOT NULL,
    data_pedido date NOT NULL DEFAULT CURRENT_DATE,
    data_prevista date 
);

CREATE TABLE IF NOT EXISTS conversas(
    id SERIAL PRIMARY KEY,
    telefone VARCHAR(20) NOT NULL,
    pergunta TEXT NOT NULL,
    resposta TEXT,
    tool_usada VARCHAR(255),
    transferiu BOOLEAN NOT NULL DEFAULT FALSE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
    
);

CREATE TABLE IF NOT EXISTS transferencias (
    id SERIAL PRIMARY KEY,
    conversa_id INT REFERENCES conversas(id),
    telefone VARCHAR(20) NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    data_transferencia TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atendido BOOLEAN NOT NULL DEFAULT FALSE    
);