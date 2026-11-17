/* =====================================================================
   PROJETO INTERDISCIPLINAR - BANCO DE DADOS I (ADS, 2º semestre/2026)
   Sistema de Gestão de Demandas de Articulação - CRIE / Extrema-MG
   Equipe Cortex: Gabriel Ribeiro de Borba, Henry Claro Maruca,
   Inácio Fontes Bueno, Miguel Vaz de Souza, Vinícius Fatichi Marrocos

   Script 01: criação do banco e das tabelas (DDL) - MySQL 8
   Recorte de BD1 com 6 tabelas: usuario, assistido, assistido_profissional,
   reuniao, demanda e evolucao. Nomes iguais aos do back-end do sistema.
   ===================================================================== */

-- Apaga o banco, se já existir, para o script poder ser executado do zero
DROP DATABASE IF EXISTS crie_demandas;

CREATE DATABASE crie_demandas
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE crie_demandas;

/* ---------------------------------------------------------------------
   USUARIO: profissional ou membro da direção que acessa o sistema.
   Senha guardada somente como hash (RN12). Não é excluído, é desativado (RN11).
   --------------------------------------------------------------------- */
CREATE TABLE usuario (
  id          INT           NOT NULL AUTO_INCREMENT,
  nome        VARCHAR(120)  NOT NULL,
  email       VARCHAR(254)  NOT NULL,
  senha_hash  VARCHAR(255)  NOT NULL,
  perfil      ENUM('direcao', 'assistente_social', 'equipe_pedagogica') NOT NULL,
  ativo       BOOLEAN       NOT NULL DEFAULT TRUE,
  criado_em   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE (email)
);

/* ---------------------------------------------------------------------
   ASSISTIDO: pessoa atendida pelo CRIE. Só o nome de tratamento
   (minimização de dados da LGPD, decisão A3 da equipe).
   --------------------------------------------------------------------- */
CREATE TABLE assistido (
  id               INT           NOT NULL AUTO_INCREMENT,
  nome_tratamento  VARCHAR(120)  NOT NULL,
  ativo            BOOLEAN       NOT NULL DEFAULT TRUE,
  criado_em        DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

/* ---------------------------------------------------------------------
   ASSISTIDO_PROFISSIONAL: tabela associativa do relacionamento N:N
   "profissional acompanha assistido", com atributo próprio (data_inicio).
   --------------------------------------------------------------------- */
CREATE TABLE assistido_profissional (
  assistido_id     INT   NOT NULL,
  profissional_id  INT   NOT NULL,
  data_inicio      DATE  NOT NULL,
  PRIMARY KEY (assistido_id, profissional_id),
  FOREIGN KEY (assistido_id) REFERENCES assistido (id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (profissional_id) REFERENCES usuario (id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

/* ---------------------------------------------------------------------
   REUNIAO: reunião semanal de um setor (RN01).
   O setor é um domínio fechado de três valores.
   --------------------------------------------------------------------- */
CREATE TABLE reuniao (
  id         INT       NOT NULL AUTO_INCREMENT,
  data       DATE      NOT NULL,
  setor      ENUM('pedagogico', 'saude', 'convivencia') NOT NULL,
  criado_em  DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

/* ---------------------------------------------------------------------
   DEMANDA: situação levantada em reunião que exige articulação.
   Estado em domínio fechado (RN05) e sempre nasce 'aberta' (RN06).
   --------------------------------------------------------------------- */
CREATE TABLE demanda (
  id              INT          NOT NULL AUTO_INCREMENT,
  descricao       TEXT         NOT NULL,
  categoria       VARCHAR(80)  NULL,
  prioridade      ENUM('baixa', 'media', 'alta') NOT NULL,
  prazo           DATE         NOT NULL,
  estado          ENUM('aberta', 'em_andamento', 'aguardando_terceiros', 'concluida', 'cancelada')
                  NOT NULL DEFAULT 'aberta',
  responsavel_id  INT          NOT NULL,   -- 1:N com USUARIO (é responsável por)
  reuniao_id      INT          NOT NULL,   -- 1:N com REUNIAO (origina)
  assistido_id    INT          NULL,       -- 1:N opcional com ASSISTIDO (RN03)
  criado_em       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  atualizado_em   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (responsavel_id) REFERENCES usuario (id)   ON UPDATE CASCADE,
  FOREIGN KEY (reuniao_id)     REFERENCES reuniao (id)   ON UPDATE CASCADE,
  FOREIGN KEY (assistido_id)   REFERENCES assistido (id) ON UPDATE CASCADE
);

/* ---------------------------------------------------------------------
   EVOLUCAO: anotação de acompanhamento do assistido, feita por um profissional.
   Não é apagada nem editada: corrigir é lançar uma nova versão que aponta
   para a original (retifica_id). O UNIQUE em retifica_id faz o
   autorrelacionamento ser 1:1: cada versão é retificada no máximo uma vez.
   --------------------------------------------------------------------- */
CREATE TABLE evolucao (
  id               INT          NOT NULL AUTO_INCREMENT,
  assistido_id     INT          NOT NULL,   -- 1:N com ASSISTIDO (possui)
  profissional_id  INT          NOT NULL,   -- 1:N com USUARIO (escreve)
  data             DATE         NOT NULL,
  area_atuacao     VARCHAR(80)  NOT NULL,
  descricao        TEXT         NOT NULL,
  ocorrido_em      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  retifica_id      INT          NULL,       -- 1:1 com a própria EVOLUCAO (retifica)
  PRIMARY KEY (id),
  FOREIGN KEY (assistido_id)    REFERENCES assistido (id) ON UPDATE CASCADE,
  FOREIGN KEY (profissional_id) REFERENCES usuario (id)   ON UPDATE CASCADE
);

-- A chave do autorrelacionamento é acrescentada com ALTER TABLE:
-- UNIQUE garante o 1:1 e a FOREIGN KEY garante que a versão retificada existe.
ALTER TABLE evolucao
  ADD CONSTRAINT uq_evolucao_retifica UNIQUE (retifica_id),
  ADD CONSTRAINT fk_evolucao_retifica FOREIGN KEY (retifica_id)
      REFERENCES evolucao (id) ON UPDATE CASCADE;

-- Conferência da estrutura criada
SHOW TABLES;
DESCRIBE demanda;
DESCRIBE evolucao;
