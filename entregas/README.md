# Entregas do projeto integrado (2º semestre de 2026)

O mesmo sistema (Sistema de Demandas do CRIE) é avaliado em cinco disciplinas e em Extensão. Esta pasta junta, para cada entrega:
- o que o professor pede, com a fonte;
- o checklist do que já está feito;
- os arquivos finais ou o lugar onde eles estão no repositório.

- **Exigências literais, com citação e fonte:** [EXIGENCIAS_OFICIAIS.md](EXIGENCIAS_OFICIAIS.md).
- **Avaliação do projeto em 23/11, com riscos e plano:** [AVALIACAO_2026-11-23.md](AVALIACAO_2026-11-23.md).

## Calendário

| Data | Disciplina | Entrega | Peso | Pasta |
|---|---|---|---|---|
| 25/11 (qua) | Engenharia de Software | Trabalho final no template Volere + apresentação | não publicado | [engenharia-de-software/](engenharia-de-software/) |
| 26/11 (qui) | Extensão 2 | ET5: sistema final, board Kanban e relatório v5 | 20% da média | [extensao/](extensao/) |
| 29/11 (dom) 23:59 | Banco de Dados 1 | Projeto interdisciplinar: .zip com PDF e .sql. **Cada integrante envia pelo próprio login** | até 8 pontos | [bd1/](bd1/) |
| 30/11 (seg) | Banco de Dados 1 | Seminário de 20 min | 1,0 dos 8 | [bd1/](bd1/) |
| 01/12 (ter) 23:59 | POO | Projeto: API Flask OO + SQLite3 + apresentação | 9,0 | [poo/](poo/) |
| 04/12 (sex) 23:59 | Front End | Projeto: React consumindo a API + apresentação | 10,0 | [front-end/](front-end/) |
| a confirmar | IHC | Projeto final: protótipo + avaliação de usabilidade | 40% | [ihc/](ihc/) |

## Regras que valem para todas
- **Só dados fictícios:** código, prints, testes e apresentação. O CRIE atende menores de idade e há dados de saúde (RNF06, RNF07, LGPD).
- **Apresentações de POO e Front End** (texto idêntico nos dois enunciados): até 20 min; todos apresentam; mostrar o front, o back e os dados gravados no banco; mostrar a divisão de tarefas; apresentar um trecho relevante do código.
- **Links:** conferir o link da Vercel num navegador sem login antes de entregar.
- **Arquivos .zip:**
  - gerados com `git archive`, que já deixa de fora `node_modules`, `.venv` e `.env`;
  - os comandos estão no README de cada pasta.
- **Testes automatizados:** rodam em todo PR (`.github/workflows/testes.yml`). Em 23/11: 587 testes do back-end e 4 do front-end aprovados.
