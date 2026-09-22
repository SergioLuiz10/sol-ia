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