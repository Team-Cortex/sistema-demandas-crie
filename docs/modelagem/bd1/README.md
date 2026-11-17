# Projeto Interdisciplinar de Banco de Dados I (Equipe Cortex)

Sistema de Gestão de Demandas de Articulação do CRIE / APAE de Extrema-MG. Parte de BD1 (Profª Letícia, IFSP Bragança Paulista, ADS 2º semestre de 2026). Entrega no Moodle até 29/11/2026; seminário em 30/11/2026.

## O que tem aqui

| Pasta/arquivo | Conteúdo |
|---|---|
| `docs/modelagem/sql/01_criacao_banco.sql` | DROP/CREATE DATABASE, CREATE TABLE das 6 tabelas, ALTER TABLE |
| `docs/modelagem/sql/02_carga_dados.sql` | 103 registros fictícios |
| `docs/modelagem/sql/03_consultas.sql` | 17 consultas comentadas |
| `docs/modelagem/sql/04_manutencao_dados.sql` | INSERT, UPDATE e DELETE de manutenção |
| `docs/modelagem/bd1/Documento_BD1_Equipe_Cortex.pdf` | Documento único: capa, universo de discurso, DER, notação textual, 3FN, dicionário, scripts e consultas com resultado |
| `docs/modelagem/bd1/DER_recorte_BD1.svg` | DER do recorte (notação de Heuser) |
| `docs/modelagem/bd1/Slides_Seminario_BD1_Equipe_Cortex.pdf` | 27 slides para os 20 minutos |
| `docs/modelagem/bd1/GUIA_APRESENTACAO.md` | Divisão da fala, fala de cada consulta, perguntas prováveis |

## Critérios do enunciado e onde estão atendidos

| Critério (pontos) | Onde |
|---|---|
| Apresentação (1,0) | slides + guia; cada um explica o processamento das próprias consultas |
| Universo de discurso, DER, notação textual (1,0) | seções 2, 3 e 4 do documento |
| Scripts create/drop/alter e carga com diversidade (1,0) | `01` e `02`; seção 5 |
| Mínimo de 12 consultas diferentes, com datas, matemática, junção e GROUP BY (5,0) | 17 consultas em `03`; seção 6, cada uma com resultado e explicação |
| 4 a 6 tabelas; tipos numérico, texto e data; 1:1, 1:N e N:N | 6 tabelas; seção 3.1 e dicionário (seção 4.3) |

## Como executar

MySQL 8 (Workbench ou linha de comando), nesta ordem: `01`, `02`, `03`, `04`. Testado do zero no MySQL 8.4, sem erro.

## Observações

- Os nomes de tabelas e colunas seguem o back-end do sistema (`backend/app/models`), para os dois bancos contarem a mesma história.
- Todos os dados são fictícios.
- Material elaborado com apoio de IA a partir das aulas de BD1 e dos documentos da equipe (minimundo, DER, requisitos). Revisar em equipe antes de entregar.
