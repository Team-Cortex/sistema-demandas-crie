/* =====================================================================
   PROJETO INTERDISCIPLINAR - BANCO DE DADOS I
   Sistema de Gestão de Demandas de Articulação - CRIE / Extrema-MG

   Script 02: carga de dados (DML) - executar depois do script 01
   Todos os dados são FICTÍCIOS (regra do minimundo: o sistema trata dados
   de saúde de pessoas com deficiência). E-mails usam o domínio reservado
   exemplo.test, como no seed do back-end.
   ===================================================================== */

USE crie_demandas;

-- USUARIO: 2 da direção, 7 profissionais (1 desativado). Senhas fictícias, gravadas só como hash.
INSERT INTO usuario (nome, email, senha_hash, perfil, ativo, criado_em) VALUES
  ('Helena Duarte Campos',    'helena.campos@exemplo.test',    SHA2('ficticia-01', 256), 'direcao',           TRUE,  '2025-01-10 09:00:00'),
  ('Rafael Antunes Prado',    'rafael.prado@exemplo.test',     SHA2('ficticia-02', 256), 'direcao',           TRUE,  '2025-01-10 09:05:00'),
  ('Beatriz Lemos Furtado',   'beatriz.furtado@exemplo.test',  SHA2('ficticia-03', 256), 'equipe_pedagogica', TRUE,  '2025-01-15 08:30:00'),
  ('Camila Rocha Vianna',     'camila.vianna@exemplo.test',    SHA2('ficticia-04', 256), 'equipe_pedagogica', TRUE,  '2025-02-03 08:30:00'),
  ('Fernanda Ishikawa Lopes', 'fernanda.lopes@exemplo.test',   SHA2('ficticia-05', 256), 'equipe_pedagogica', TRUE,  '2025-03-17 13:00:00'),
  ('Juliana Cardoso Neves',   'juliana.neves@exemplo.test',    SHA2('ficticia-06', 256), 'assistente_social', TRUE,  '2025-01-15 08:45:00'),
  ('Marcos Vieira Salgado',   'marcos.salgado@exemplo.test',   SHA2('ficticia-07', 256), 'assistente_social', TRUE,  '2025-02-03 09:10:00'),
  ('Daniel Moura Teixeira',   'daniel.teixeira@exemplo.test',  SHA2('ficticia-08', 256), 'assistente_social', TRUE,  '2025-06-02 10:00:00'),
  ('Patrícia Gomes Ribeiro',  'patricia.ribeiro@exemplo.test', SHA2('ficticia-09', 256), 'assistente_social', FALSE, '2025-02-03 09:20:00'),
  ('Otávio Brandão Freitas',  'otavio.freitas@exemplo.test',   SHA2('ficticia-10', 256), 'equipe_pedagogica', TRUE,  '2026-07-20 14:00:00');

-- ASSISTIDO: somente o nome de tratamento (fictício)
INSERT INTO assistido (nome_tratamento, ativo, criado_em) VALUES
  ('Ana Clara M.',  TRUE,  '2024-02-19 10:00:00'),
  ('Bruno H.',      TRUE,  '2023-03-06 10:00:00'),
  ('Carolina D.',   TRUE,  '2025-05-12 09:30:00'),
  ('Davi L.',       TRUE,  '2022-08-15 14:00:00'),
  ('Eduarda S.',    TRUE,  '2026-02-23 08:30:00'),
  ('Felipe A.',     TRUE,  '2021-04-05 15:00:00'),
  ('Gabriela N.',   TRUE,  '2024-08-05 09:00:00'),
  ('Heitor G.',     TRUE,  '2026-08-03 08:00:00'),
  ('Isabela C.',    FALSE, '2020-03-02 10:30:00'),
  ('João Pedro M.', TRUE,  '2025-09-01 13:30:00'),
  ('Larissa F.',    TRUE,  '2024-01-15 11:00:00'),
  ('Mateus H.',     TRUE,  '2025-11-03 10:00:00');

-- ASSISTIDO_PROFISSIONAL (N:N): quem acompanha quem e desde quando
INSERT INTO assistido_profissional (assistido_id, profissional_id, data_inicio) VALUES
  (1, 3, '2024-02-19'), (1, 4, '2025-03-10'), (1, 6, '2025-08-04'),
  (2, 3, '2023-03-06'), (2, 7, '2025-02-17'),
  (3, 5, '2025-05-12'), (3, 4, '2025-05-12'),
  (4, 8, '2022-08-15'), (4, 6, '2024-09-02'),
  (5, 5, '2026-02-23'), (5, 4, '2026-02-23'),
  (6, 7, '2021-04-05'), (6, 8, '2023-06-12'),
  (7, 4, '2024-08-05'),
  (8, 5, '2026-08-03'),
  (9, 6, '2020-03-02'),
  (10, 3, '2025-09-01'), (10, 8, '2026-03-16'),
  (11, 7, '2024-01-15'),
  (12, 6, '2025-11-03'), (12, 4, '2025-11-03');

-- REUNIAO: reuniões semanais dos três setores (ids em ordem cronológica)
INSERT INTO reuniao (data, setor, criado_em) VALUES
  ('2026-08-05', 'pedagogico',  '2026-08-05 17:30:00'),
  ('2026-08-12', 'saude',       '2026-08-12 17:30:00'),
  ('2026-08-19', 'convivencia', '2026-08-19 17:30:00'),
  ('2026-09-02', 'pedagogico',  '2026-09-02 17:30:00'),
  ('2026-09-09', 'saude',       '2026-09-09 17:30:00'),
  ('2026-09-16', 'convivencia', '2026-09-16 17:30:00'),   -- não gerou demandas
  ('2026-10-07', 'pedagogico',  '2026-10-07 17:30:00'),
  ('2026-10-14', 'saude',       '2026-10-14 17:30:00'),
  ('2026-10-21', 'convivencia', '2026-10-21 17:30:00'),
  ('2026-11-04', 'pedagogico',  '2026-11-04 17:30:00'),
  ('2026-11-11', 'saude',       '2026-11-11 17:30:00'),
  ('2026-11-12', 'convivencia', '2026-11-12 17:30:00'),
  ('2026-11-13', 'pedagogico',  '2026-11-13 17:30:00');   -- não gerou demandas

-- DEMANDA: criada no dia da reunião de origem (RN02).
-- atualizado_em = última mudança; nas concluídas e canceladas, é o dia do encerramento.
INSERT INTO demanda (descricao, categoria, prioridade, prazo, estado, responsavel_id, reuniao_id, assistido_id, criado_em, atualizado_em) VALUES
  ('Solicitar à escola municipal o plano de atendimento educacional especializado (AEE)', 'Educação',           'alta',  '2026-08-26', 'concluida',            3,  1, 1,    '2026-08-05 18:00:00', '2026-08-24 10:15:00'),
  ('Convocar a família para reunião sobre faltas recorrentes',                           'Família',            'media', '2026-08-19', 'concluida',            4,  1, 2,    '2026-08-05 18:05:00', '2026-08-18 14:00:00'),
  ('Verificar se a família está referenciada no CRAS',                                   'Assistência social', 'media', '2026-09-05', 'concluida',            6,  1, 10,   '2026-08-05 18:10:00', '2026-09-15 09:30:00'),
  ('Agendar avaliação com neuropediatra na unidade de saúde',                            'Saúde',              'alta',  '2026-09-12', 'concluida',            8,  2, 4,    '2026-08-12 18:00:00', '2026-10-02 16:50:00'),
  ('Solicitar cadeira de banho adaptada à Secretaria de Saúde',                          'Saúde',              'media', '2026-09-30', 'aguardando_terceiros', 8,  2, 6,    '2026-08-12 18:05:00', '2026-09-03 11:00:00'),
  ('Revisar o protocolo interno de administração de medicamentos',                       'Saúde',              'baixa', '2026-09-15', 'concluida',            8,  2, NULL, '2026-08-12 18:10:00', '2026-09-10 15:20:00'),
  ('Acionar o Conselho Tutelar sobre suspeita de negligência',                           'Assistência social', 'alta',  '2026-08-26', 'concluida',            6,  3, 7,    '2026-08-19 18:00:00', '2026-08-25 17:00:00'),
  ('Encerrar o atendimento e transferir o prontuário ao serviço adulto',                 'Documentação',       'media', '2026-09-02', 'concluida',            6,  3, 9,    '2026-08-19 18:05:00', '2026-08-31 10:00:00'),
  ('Organizar transporte para as atividades do serviço de convivência',                  'Transporte',         'media', '2026-09-19', 'cancelada',            7,  3, NULL, '2026-08-19 18:10:00', '2026-09-25 08:45:00'),
  ('Adaptar material didático com comunicação alternativa',                              'Educação',           'media', '2026-10-02', 'concluida',            4,  4, 3,    '2026-09-02 18:00:00', '2026-09-29 13:30:00'),
  ('Encaminhar laudo atualizado para a escola regular',                                  'Documentação',       'alta',  '2026-09-16', 'concluida',            3,  4, 1,    '2026-09-02 18:05:00', '2026-09-30 09:00:00'),
  ('Agendar terapia fonoaudiológica semanal',                                            'Saúde',              'media', '2026-09-30', 'concluida',            5,  5, 3,    '2026-09-09 18:00:00', '2026-09-28 14:40:00'),
  ('Solicitar órtese de membro inferior ao Centro Especializado em Reabilitação',        'Saúde',              'alta',  '2026-10-31', 'aguardando_terceiros', 8,  5, 4,    '2026-09-09 18:05:00', '2026-09-22 10:10:00'),
  ('Orientar a família sobre o Benefício de Prestação Continuada (BPC)',                 'Assistência social', 'media', '2026-10-09', 'concluida',            6,  5, 5,    '2026-09-09 18:10:00', '2026-10-20 11:30:00'),
  ('Revisar o plano de ensino individualizado (PEI) com a escola',                       'Educação',           'alta',  '2026-11-07', 'em_andamento',         3,  7, 10,   '2026-10-07 18:00:00', '2026-10-15 17:20:00'),
  ('Solicitar transporte escolar adaptado à Prefeitura',                                 'Transporte',         'alta',  '2026-11-20', 'aguardando_terceiros', 7,  7, 2,    '2026-10-07 18:05:00', '2026-10-28 09:40:00'),
  ('Atualizar o cadastro de contatos dos responsáveis legais',                           'Documentação',       'baixa', '2026-12-04', 'aberta',               1,  7, NULL, '2026-10-07 18:10:00', '2026-10-07 18:10:00'),
  ('Acompanhar o resultado de exames na unidade básica de saúde',                        'Saúde',              'media', '2026-11-14', 'concluida',            5,  8, 5,    '2026-10-14 18:00:00', '2026-11-10 15:00:00'),
  ('Encaminhar para avaliação psicológica',                                              'Saúde',              'alta',  '2026-10-28', 'concluida',            8,  8, 12,   '2026-10-14 18:05:00', '2026-10-27 16:30:00'),
  ('Verificar com a família a vacinação em atraso',                                      'Saúde',              'baixa', '2026-12-01', 'em_andamento',         5,  8, 7,    '2026-10-14 18:10:00', '2026-10-30 10:00:00'),
  ('Mediar conflito familiar relatado pela equipe',                                      'Família',            'alta',  '2026-11-04', 'concluida',            6,  9, 12,   '2026-10-21 18:00:00', '2026-11-12 10:30:00'),
  ('Inscrever em oficina de música do CRAS',                                             'Assistência social', 'baixa', '2026-12-11', 'aberta',               7,  9, 6,    '2026-10-21 18:05:00', '2026-10-21 18:05:00'),
  ('Solicitar segunda via de documento de identidade',                                   'Documentação',       'media', '2026-11-21', 'em_andamento',         7,  9, 2,    '2026-10-21 18:10:00', '2026-11-03 14:15:00'),
  ('Planejar a adaptação da rotina escolar após cirurgia',                               'Educação',           'media', '2026-12-05', 'em_andamento',         4, 10, 7,    '2026-11-04 18:00:00', '2026-11-06 09:00:00'),
  ('Convocar a família para a devolutiva semestral',                                     'Família',            'baixa', '2026-12-18', 'aberta',               3, 10, 1,    '2026-11-04 18:05:00', '2026-11-04 18:05:00'),
  ('Solicitar consulta com ortopedista pelo SUS',                                        'Saúde',              'alta',  '2026-11-25', 'aguardando_terceiros', 8, 11, 10,   '2026-11-11 18:00:00', '2026-11-12 10:20:00'),
  ('Cancelar pedido duplicado de transporte sanitário',                                  'Transporte',         'baixa', '2026-11-18', 'cancelada',            8, 11, NULL, '2026-11-11 18:05:00', '2026-11-12 08:10:00'),
  ('Articular vaga em curso de qualificação profissional',                               'Assistência social', 'media', '2026-12-12', 'aberta',               6, 12, 6,    '2026-11-12 18:00:00', '2026-11-12 18:00:00'),
  ('Reunir a rede para discutir caso de evasão escolar',                                 'Educação',           'alta',  '2026-12-03', 'aberta',               6, 12, 4,    '2026-11-12 18:05:00', '2026-11-12 18:05:00');

-- EVOLUCAO: 14 lançamentos originais e 3 retificações (15, 16 e 17).
-- A 16 retifica a 5, e a 17 retifica a 16: uma cadeia de versões (1:1).
INSERT INTO evolucao (assistido_id, profissional_id, data, area_atuacao, descricao, ocorrido_em, retifica_id) VALUES
  (1,  3, '2026-08-10', 'Pedagógica',     'Participou da atividade de leitura com apoio de pictogramas.',              '2026-08-10 16:20:00', NULL),
  (1,  4, '2026-09-14', 'Pedagógica',     'Concluiu a sequência de atividades de coordenação motora fina.',             '2026-09-14 15:05:00', NULL),
  (2,  7, '2026-08-20', 'Serviço social', 'Família compareceu e assinou o termo de acompanhamento.',                   '2026-08-20 10:40:00', NULL),
  (3,  5, '2026-09-11', 'Fonoaudiologia', 'Ampliou o uso da prancha de comunicação em sala.',                          '2026-09-11 14:00:00', NULL),
  (3,  5, '2026-10-09', 'Fonoaudiologia', 'Iniciou a produção de frases de duas palavras.',                            '2026-10-09 14:10:00', NULL),
  (4,  8, '2026-08-13', 'Saúde',          'Aguardando retorno da consulta com o neuropediatra.',                       '2026-08-13 11:30:00', NULL),
  (4,  8, '2026-10-02', 'Saúde',          'Consulta realizada; orientações repassadas à família.',                     '2026-10-02 16:45:00', NULL),
  (5,  4, '2026-09-03', 'Pedagógica',     'Adaptação inicial à rotina da sala concluída.',                             '2026-09-03 13:50:00', NULL),
  (6,  7, '2026-09-17', 'Convivência',    'Participou da oficina de música com boa interação.',                        '2026-09-17 15:30:00', NULL),
  (7,  4, '2026-10-08', 'Pedagógica',     'Ausente três dias na semana; família informada.',                           '2026-10-08 12:00:00', NULL),
  (10, 3, '2026-10-15', 'Pedagógica',     'Revisão das metas do plano de ensino com a escola.',                        '2026-10-15 17:10:00', NULL),
  (12, 6, '2026-10-22', 'Serviço social', 'Escuta da família sobre conflito no ambiente doméstico.',                   '2026-10-22 09:30:00', NULL),
  (12, 6, '2026-11-05', 'Serviço social', 'Mediação realizada; combinados registrados com a família.',                 '2026-11-05 10:15:00', NULL),
  (9,  6, '2026-08-21', 'Serviço social', 'Atendimento encerrado e prontuário transferido.',                           '2026-08-21 11:00:00', NULL),
  (7,  4, '2026-10-08', 'Pedagógica',     'Ausente dois dias na semana (correção); família informada.',                '2026-10-09 08:40:00', 10),
  (3,  5, '2026-10-09', 'Fonoaudiologia', 'Iniciou a produção de frases de duas e três palavras.',                     '2026-10-10 09:15:00', 5),
  (3,  5, '2026-10-09', 'Fonoaudiologia', 'Iniciou a produção de frases de duas e três palavras com apoio visual.',     '2026-10-12 08:05:00', 16),
  (11, 7, '2026-11-10', 'Convivência',    'Primeira participação no grupo de convivência de adultos.',                 '2026-11-10 15:00:00', NULL);

-- Conferência: quantidade de registros em cada tabela
SELECT COUNT(*) AS usuarios       FROM usuario;
SELECT COUNT(*) AS assistidos     FROM assistido;
SELECT COUNT(*) AS acompanhamentos FROM assistido_profissional;
SELECT COUNT(*) AS reunioes       FROM reuniao;
SELECT COUNT(*) AS demandas       FROM demanda;
SELECT COUNT(*) AS evolucoes      FROM evolucao;
