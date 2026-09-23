INSERT INTO bairros (nome_bairro, prazo_dias) VALUES
    ('Pituba', 2),
    ('Barra', 2),
    ('Rio Vermelho', 2),
    ('Itaigara', 2),
    ('Caminho das Árvores', 1),
    ('Brotas', 3),
    ('Federação', 3),
    ('Cabula', 4),
    ('Itapuã', 4),
    ('Stella Maris', 4),
    ('São Cristóvão', 5),
    ('Cajazeiras', 5),
    ('Paripe', 6),
    ('Subúrbio Ferroviário', 6),
    ('Ilha de Maré', 8)
ON CONFLICT (nome_bairro) DO NOTHING;

INSERT INTO pedidos (numero_pedido, cliente, telefone, bairro_id, status, data_pedido, data_prevista) VALUES
    ('001', 'João Silva', '71933333333', (SELECT id FROM bairros WHERE nome_bairro = 'Pituba'), 'separando', CURRENT_DATE, CURRENT_DATE + INTERVAL '2 days'),
    ('002', 'Maria Oliveira', '71988888888', (SELECT id FROM bairros WHERE nome_bairro = 'Barra'), 'em transporte', CURRENT_DATE, CURRENT_DATE + INTERVAL '2 days'),
    ('003', 'Carlos Souza', '71977777777', (SELECT id FROM bairros WHERE nome_bairro = 'Rio Vermelho'), 'entregue', CURRENT_DATE - INTERVAL '7 days', CURRENT_DATE - INTERVAL '5 days' ),
    ('004', 'Ana Lima', '71966666666', (SELECT id FROM bairros WHERE nome_bairro = 'Itaigara'), 'cancelado', CURRENT_DATE, null),
    ('005', 'Pedro Santos', '71955555555', (SELECT id FROM bairros WHERE nome_bairro = 'Cajazeiras'), 'separando', CURRENT_DATE, CURRENT_DATE + INTERVAL '5 days'),
    ('006', 'Lucas Pereira', '71944444444', (SELECT id FROM bairros WHERE nome_bairro = 'Ilha de Maré'), 'em transporte', CURRENT_DATE, CURRENT_DATE + INTERVAL '8 days'),
    ('007', 'Ana Luiza', '71999999999', (SELECT id FROM bairros WHERE nome_bairro = 'Barra'), 'cancelado', CURRENT_DATE, null),
    ('008', 'Ana Luiza', '71999999999', (SELECT id FROM bairros WHERE nome_bairro = 'Cabula'), 'entregue', CURRENT_DATE - INTERVAL '6 days', CURRENT_DATE - INTERVAL '4 days')
ON CONFLICT (numero_pedido) DO NOTHING;





