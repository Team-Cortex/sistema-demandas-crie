# Banco de Dados 1: projeto interdisciplinar

**Profª Letícia Souza Netto Brandi.**
- **Envio no Moodle:** até 29/11/2026, 23:59.
- **Seminário:** 30/11/2026.
- **Valor:** até 8 pontos. A média é (A1 + A2 + SQL + SIM + Proj) / 2.
- **Fontes:** `2026s2Projeto_BD_interdisciplinar2.modulo.pdf` (Moodle de BD1, semana de 30/11) e `Aula00 - Planejamento.pdf`, pág. 5.

## O que o enunciado pede

| Critério | Pontos | Onde está |
|---|---|---|
| Apresentação ("explicar o processamento das consultas", 20 min) | 1,0 | [slides](../../docs/modelagem/bd1/Slides_Seminario_BD1_Equipe_Cortex.pdf) e [guia da fala](../../docs/modelagem/bd1/GUIA_APRESENTACAO.md) |
| "Universo de discurso… Diagrama entidade relacionamento… Notação textual das tabelas" | 1,0 | Seções 2 a 4 do [documento](../../docs/modelagem/bd1/Documento_BD1_Equipe_Cortex.pdf) |
| Scripts "create table/database/drop/alter table" e "Popular as tabelas com diversidade de registros" | 1,0 | [`01_criacao_banco.sql`](../../docs/modelagem/sql/01_criacao_banco.sql) e [`02_carga_dados.sql`](../../docs/modelagem/sql/02_carga_dados.sql) (103 registros fictícios) |
| "mínimo de 12 queries… diferentes nas suas formas e conteúdo… funções matemáticas e ou datas, ligação de tabelas/group by" | 5,0 | 17 consultas em [`03_consultas.sql`](../../docs/modelagem/sql/03_consultas.sql), com o propósito de cada uma nos comentários |
| 4 a 6 tabelas; tipos numérico, texto e data; relacionamentos 1:1, 1:N e N:N | regra | 6 tabelas; seção 3.1 e dicionário de dados (seção 4.3) |

## Pacote de envio

[`BD1_Projeto_Interdisciplinar_Equipe_Cortex.zip`](BD1_Projeto_Interdisciplinar_Equipe_Cortex.zip), no formato pedido: um único PDF (com capa e os nomes) mais os `.sql` separados. Contém:
- `Documento_BD1_Equipe_Cortex.pdf` (46 páginas, ABNT);
- `01_criacao_banco.sql`, `02_carga_dados.sql`, `03_consultas.sql`, `04_manutencao_dados.sql`.

Se algum arquivo mudar, refaça o pacote a partir da raiz do repositório:

```bash
cd docs/modelagem && zip -j ../../entregas/bd1/BD1_Projeto_Interdisciplinar_Equipe_Cortex.zip bd1/Documento_BD1_Equipe_Cortex.pdf sql/*.sql
```

## Checklist

- [x] Documento ABNT com capa, folha de rosto (nome completo da professora, corrigido em 23/11), universo de discurso, DER, notação textual, 3FN, dicionário, scripts e as 17 consultas com resultado.
- [x] Scripts testados do zero no MySQL 8.4, sem erro.
- [x] Slides de 27 páginas e guia com a divisão da fala.
- [ ] **Cada integrante** envia o .zip no Moodle pelo próprio login, até 29/11.
- [ ] Ensaio do seminário: cada um explica o processamento das próprias consultas.

As ferramentas que geram o documento e os slides estão em [`docs/modelagem/bd1/ferramentas/`](../../docs/modelagem/bd1/ferramentas/LEIA-ME.md).
