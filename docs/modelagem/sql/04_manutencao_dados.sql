/* =====================================================================
   PROJETO INTERDISCIPLINAR - BANCO DE DADOS I
   Sistema de Gestão de Demandas de Articulação - CRIE / Extrema-MG

   Script 04: manutenção dos dados (INSERT, UPDATE, DELETE)
   Operações do dia a dia do sistema, respeitando as regras do minimundo:
   demandas e evoluções nunca são apagadas (RN10), usuários são
   desativados e não excluídos (RN11). Executar depois dos scripts 01 e 02
   (e depois do 03, se quiser ver as consultas com os dados originais).
   ===================================================================== */

USE crie_demandas;

-- 1) INSERT: nova reunião do setor de saúde e uma demanda nascida nela.
--    A demanda não informa o estado: o DEFAULT 'aberta' é aplicado (RN06).
INSERT INTO reuniao (data, setor) VALUES ('2026-11-18', 'saude');

INSERT INTO demanda (descricao, categoria, prioridade, prazo, responsavel_id, reuniao_id, assistido_id)
VALUES ('Solicitar avaliação de órtese para membro superior', 'Saúde', 'media', '2026-12-16',
        8, (SELECT MAX(id) FROM reuniao), 8);

SELECT id, descricao, estado, criado_em FROM demanda WHERE assistido_id = 8;

-- 2) UPDATE: mudança de estado da demanda 13 (a órtese chegou e foi entregue).
--    atualizado_em muda sozinho (ON UPDATE CURRENT_TIMESTAMP).
UPDATE demanda
SET estado = 'concluida'
WHERE id = 13;

SELECT id, estado, atualizado_em FROM demanda WHERE id = 13;

-- 3) UPDATE: reatribuição do responsável de todas as demandas em aberto de uma
--    profissional para outra (por exemplo, durante as férias da titular).
UPDATE demanda
SET responsavel_id = 6
WHERE responsavel_id = 7
  AND estado NOT IN ('concluida', 'cancelada');

-- 4) UPDATE no lugar de DELETE: o usuário é desativado, não excluído (RN11),
--    para preservar a autoria dos registros antigos.
UPDATE usuario
SET ativo = FALSE
WHERE email = 'otavio.freitas@exemplo.test';

-- 5) DELETE: um vínculo de acompanhamento lançado por engano é removido.
--    Apagar o vínculo não apaga o assistido nem o profissional.
DELETE FROM assistido_profissional
WHERE assistido_id = 5
  AND profissional_id = 4;

SELECT COUNT(*) AS profissionais_da_eduarda
FROM assistido_profissional
WHERE assistido_id = 5;

-- 6) Integridade referencial: esta exclusão é RECUSADA pelo banco,
--    porque a reunião 1 tem demandas ligadas a ela (a chave estrangeira
--    de demanda não tem ON DELETE CASCADE). Resultado esperado: erro 1451.
-- DELETE FROM reuniao WHERE id = 1;
