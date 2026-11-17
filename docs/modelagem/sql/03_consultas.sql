/* =====================================================================
   PROJETO INTERDISCIPLINAR - BANCO DE DADOS I
   Sistema de Gestão de Demandas de Articulação - CRIE / Extrema-MG

   Script 03: consultas (SELECT) - executar depois dos scripts 01 e 02
   17 consultas, cada uma com propósito e forma diferentes.
   As consultas com CURDATE() dependem do dia em que são executadas;
   os resultados do documento foram obtidos com a data do seminário
   (30/11/2026). Para reproduzir exatamente, rode antes:
       SET TIMESTAMP = UNIX_TIMESTAMP('2026-11-30 19:00:00');
   ===================================================================== */

USE crie_demandas;

/* ---------------------------------------------------------------------
   Q01. Demandas que envolvem o CRAS ou o Conselho Tutelar, da mais
        urgente (menor prazo) para a menos urgente.
   Comandos: LIKE com %, OR, ORDER BY
   --------------------------------------------------------------------- */
SELECT id, descricao, estado, prazo
FROM demanda
WHERE descricao LIKE '%CRAS%'
   OR descricao LIKE '%Conselho Tutelar%'
ORDER BY prazo;

/* ---------------------------------------------------------------------
   Q02. Reuniões dos setores pedagógico e saúde realizadas em outubro de
        2026, com a data no formato brasileiro.
   Comandos: IN, BETWEEN com datas, DATE_FORMAT
   --------------------------------------------------------------------- */
SELECT id,
       setor,
       DATE_FORMAT(data, '%d/%m/%Y') AS data_reuniao
FROM reuniao
WHERE setor IN ('pedagogico', 'saude')
  AND data BETWEEN '2026-10-01' AND '2026-10-31'
ORDER BY data;

/* ---------------------------------------------------------------------
   Q03. Demandas em aberto com o prazo vencido e há quantos dias estão
        atrasadas, da mais atrasada para a menos atrasada.
   Comandos: CURDATE, DATEDIFF, NOT IN, ORDER BY DESC
   --------------------------------------------------------------------- */
SELECT id,
       descricao,
       estado,
       DATE_FORMAT(prazo, '%d/%m/%Y')   AS prazo,
       DATEDIFF(CURDATE(), prazo)       AS dias_de_atraso
FROM demanda
WHERE estado NOT IN ('concluida', 'cancelada')
  AND prazo < CURDATE()
ORDER BY dias_de_atraso DESC;

/* ---------------------------------------------------------------------
   Q04. Demandas em aberto que vencem nos próximos 7 dias (alerta do painel).
   Comandos: ADDDATE com INTERVAL, BETWEEN, CURDATE, DATEDIFF
   --------------------------------------------------------------------- */
SELECT id,
       descricao,
       prioridade,
       prazo,
       DATEDIFF(prazo, CURDATE()) AS dias_restantes
FROM demanda
WHERE estado NOT IN ('concluida', 'cancelada')
  AND prazo BETWEEN CURDATE() AND ADDDATE(CURDATE(), INTERVAL 7 DAY)
ORDER BY prazo;

/* ---------------------------------------------------------------------
   Q05. Demandas de prioridade alta ligadas a um assistido, com o setor e a
        data da reunião de origem e o nome do responsável.
   Comandos: INNER JOIN entre 4 tabelas, apelidos (AS), DATE_FORMAT
   --------------------------------------------------------------------- */
SELECT d.id,
       a.nome_tratamento                     AS assistido,
       d.descricao,
       r.setor,
       DATE_FORMAT(r.data, '%d/%m/%Y')       AS reuniao,
       u.nome                                AS responsavel,
       d.estado
FROM demanda d
INNER JOIN reuniao   r ON r.id = d.reuniao_id
INNER JOIN usuario   u ON u.id = d.responsavel_id
INNER JOIN assistido a ON a.id = d.assistido_id
WHERE d.prioridade = 'alta'
ORDER BY r.data, d.id;

/* ---------------------------------------------------------------------
   Q06. Assistidos ativos que ainda não têm nenhuma demanda registrada.
   Comandos: LEFT JOIN, IS NULL (registros "sem par" na outra tabela)
   --------------------------------------------------------------------- */
SELECT a.id, a.nome_tratamento, DATE(a.criado_em) AS cadastrado_em
FROM assistido a
LEFT JOIN demanda d ON d.assistido_id = a.id
WHERE a.ativo = TRUE
  AND d.id IS NULL;

/* ---------------------------------------------------------------------
   Q07. Carga de trabalho: quantas demandas em aberto cada profissional
        ativo tem sob sua responsabilidade, incluindo quem tem zero.
   Comandos: LEFT JOIN com condição no ON, COUNT(coluna), GROUP BY
   (COUNT(d.id) não conta as linhas sem demanda, que ficam NULL)
   --------------------------------------------------------------------- */
SELECT u.nome,
       u.perfil,
       COUNT(d.id) AS demandas_em_aberto
FROM usuario u
LEFT JOIN demanda d
       ON d.responsavel_id = u.id
      AND d.estado NOT IN ('concluida', 'cancelada')
WHERE u.ativo = TRUE
GROUP BY u.id, u.nome, u.perfil
ORDER BY demandas_em_aberto DESC, u.nome;

/* ---------------------------------------------------------------------
   Q08. Tempo médio, em dias, para concluir uma demanda em cada
        prioridade, mostrando só as prioridades com média acima de 24 dias.
   Comandos: GROUP BY, HAVING, AVG, ROUND, DATEDIFF, MIN, MAX
   --------------------------------------------------------------------- */
SELECT prioridade,
       COUNT(*)                                            AS concluidas,
       ROUND(AVG(DATEDIFF(atualizado_em, criado_em)), 1)   AS media_dias,
       MIN(DATEDIFF(atualizado_em, criado_em))             AS mais_rapida,
       MAX(DATEDIFF(atualizado_em, criado_em))             AS mais_lenta
FROM demanda
WHERE estado = 'concluida'
GROUP BY prioridade
HAVING AVG(DATEDIFF(atualizado_em, criado_em)) > 24
ORDER BY media_dias DESC;

/* ---------------------------------------------------------------------
   Q09. Distribuição das demandas por setor e por estado, com o percentual
        de cada grupo sobre o total de demandas.
   Comandos: INNER JOIN, GROUP BY com duas colunas, subconsulta no SELECT,
             cálculo de percentual e ROUND
   --------------------------------------------------------------------- */
SELECT r.setor,
       d.estado,
       COUNT(*) AS quantidade,
       ROUND(COUNT(*) * 100 / (SELECT COUNT(*) FROM demanda), 1) AS percentual
FROM demanda d
INNER JOIN reuniao r ON r.id = d.reuniao_id
GROUP BY r.setor, d.estado
ORDER BY r.setor, quantidade DESC;

/* ---------------------------------------------------------------------
   Q10. Quantas demandas foram abertas em cada mês e quantas categorias
        diferentes apareceram no mês.
   Comandos: YEAR, MONTH, COUNT(DISTINCT), GROUP BY por partes da data
   --------------------------------------------------------------------- */
SELECT YEAR(criado_em)            AS ano,
       MONTH(criado_em)           AS mes,
       COUNT(*)                   AS demandas_abertas,
       COUNT(DISTINCT categoria)  AS categorias_diferentes
FROM demanda
GROUP BY YEAR(criado_em), MONTH(criado_em)
ORDER BY ano, mes;

/* ---------------------------------------------------------------------
   Q11. A demanda em aberto mais antiga, quem é o responsável e há quantos
        dias ela foi aberta.
   Comandos: subconsulta que devolve um valor (MIN) comparada com =, JOIN
   --------------------------------------------------------------------- */
SELECT d.id,
       d.descricao,
       u.nome                                AS responsavel,
       DATE(d.criado_em)                     AS aberta_em,
       DATEDIFF(CURDATE(), d.criado_em)      AS dias_em_aberto
FROM demanda d
INNER JOIN usuario u ON u.id = d.responsavel_id
WHERE d.estado NOT IN ('concluida', 'cancelada')
  AND d.criado_em = (SELECT MIN(criado_em)
                     FROM demanda
                     WHERE estado NOT IN ('concluida', 'cancelada'));

/* ---------------------------------------------------------------------
   Q12. Demandas concluídas que levaram mais dias do que a média de todas
        as concluídas.
   Comandos: subconsulta com AVG no WHERE, DATEDIFF, ROUND
   --------------------------------------------------------------------- */
SELECT id,
       descricao,
       DATEDIFF(atualizado_em, criado_em) AS dias_para_concluir,
       (SELECT ROUND(AVG(DATEDIFF(atualizado_em, criado_em)), 1)
          FROM demanda WHERE estado = 'concluida') AS media_geral
FROM demanda
WHERE estado = 'concluida'
  AND DATEDIFF(atualizado_em, criado_em) >
      (SELECT AVG(DATEDIFF(atualizado_em, criado_em))
         FROM demanda
        WHERE estado = 'concluida')
ORDER BY dias_para_concluir DESC;

/* ---------------------------------------------------------------------
   Q13. Profissionais ativos que não acompanham nenhum assistido
        (candidatos a receber novos acompanhamentos).
   Comandos: subconsulta que devolve uma lista, NOT IN
   --------------------------------------------------------------------- */
SELECT id, nome, perfil
FROM usuario
WHERE ativo = TRUE
  AND perfil <> 'direcao'
  AND id NOT IN (SELECT profissional_id FROM assistido_profissional);

/* ---------------------------------------------------------------------
   Q14. Para cada profissional, quantos assistidos acompanha e há quanto
        tempo, em meses, em média, acompanha cada um (relacionamento N:N).
   Comandos: JOIN pela tabela associativa, AVG, DATEDIFF, FLOOR, ROUND
   --------------------------------------------------------------------- */
SELECT u.nome,
       COUNT(ap.assistido_id)                                   AS assistidos,
       ROUND(AVG(DATEDIFF(CURDATE(), ap.data_inicio)) / 30, 1)  AS media_meses,
       FLOOR(MAX(DATEDIFF(CURDATE(), ap.data_inicio)) / 365)    AS anos_do_mais_antigo
FROM usuario u
INNER JOIN assistido_profissional ap ON ap.profissional_id = u.id
INNER JOIN assistido a ON a.id = ap.assistido_id
WHERE a.ativo = TRUE
GROUP BY u.id, u.nome
ORDER BY assistidos DESC, media_meses DESC;

/* ---------------------------------------------------------------------
   Q15. Evoluções retificadas: cada versão corrigida ao lado da versão que
        a corrigiu e quantos dias depois a correção foi feita (1:1).
   Comandos: autojunção (a mesma tabela duas vezes com apelidos),
             DATEDIFF, DATE_FORMAT com hora e minuto
   --------------------------------------------------------------------- */
SELECT original.id                                        AS versao_corrigida,
       nova.id                                            AS versao_nova,
       a.nome_tratamento                                  AS assistido,
       original.descricao                                 AS texto_anterior,
       nova.descricao                                     AS texto_novo,
       DATE_FORMAT(nova.ocorrido_em, '%d/%m/%Y %H:%i')    AS corrigida_em,
       DATEDIFF(nova.ocorrido_em, original.ocorrido_em)   AS dias_depois
FROM evolucao original
INNER JOIN evolucao nova ON nova.retifica_id = original.id
INNER JOIN assistido a   ON a.id = original.assistido_id
ORDER BY original.id;

/* ---------------------------------------------------------------------
   Q16. Assistidos ativos cuja evolução vigente mais recente tem mais de
        20 dias (ou seja, precisam de nova anotação). Versões já
        retificadas não contam, porque foram substituídas.
   Comandos: subconsulta NOT IN com IS NOT NULL, GROUP BY, MAX,
             HAVING com DATEDIFF
   --------------------------------------------------------------------- */
SELECT a.nome_tratamento,
       COUNT(e.id)                         AS evolucoes_vigentes,
       DATE_FORMAT(MAX(e.data), '%d/%m/%Y') AS ultima_evolucao,
       DATEDIFF(CURDATE(), MAX(e.data))    AS dias_sem_evolucao
FROM assistido a
INNER JOIN evolucao e ON e.assistido_id = a.id
WHERE a.ativo = TRUE
  AND e.id NOT IN (SELECT retifica_id FROM evolucao WHERE retifica_id IS NOT NULL)
GROUP BY a.id, a.nome_tratamento
HAVING DATEDIFF(CURDATE(), MAX(e.data)) > 20
ORDER BY dias_sem_evolucao DESC;

/* ---------------------------------------------------------------------
   Q17. Todas as reuniões, com quantas demandas cada uma originou,
        incluindo as que não originaram nenhuma.
   Comandos: RIGHT JOIN (todas as linhas da tabela da direita),
             COUNT(coluna), GROUP BY
   --------------------------------------------------------------------- */
SELECT r.id                               AS reuniao,
       r.setor,
       DATE_FORMAT(r.data, '%d/%m/%Y')    AS data,
       COUNT(d.id)                        AS demandas_originadas
FROM demanda d
RIGHT JOIN reuniao r ON r.id = d.reuniao_id
GROUP BY r.id, r.setor, r.data
ORDER BY r.data;
