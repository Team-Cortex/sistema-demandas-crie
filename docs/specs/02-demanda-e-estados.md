# Spec 02 — Demanda e estados

**Status:** fechada para a máquina de estados. A persistência espera o modelo relacional.  
Decisão de transição registrada pela frente de back-end em 13/10/2026. Se a instituição descrever outro fluxo, esta tabela é substituída, com data.

Se esta spec divergir do código, a spec vence.

---

## 1. O que o servidor faz

Todas as rotas exigem token válido.

### POST `/api/demandas`

Corpo:

| Campo | Regra | Recusa (422) |
| --- | --- | --- |
| `descricao` | obrigatória, texto não vazio | `Informe a descrição da demanda.` |
| `prioridade` | obrigatória: `baixa`, `media` ou `alta` | `Escolha a prioridade: baixa, media ou alta.` |
| `responsavel_id` | obrigatório, usuário ativo | `Informe um responsável ativo.` |
| `prazo` | obrigatório, data `AAAA-MM-DD` | `Informe o prazo.` |
| `reuniao_id` | obrigatória, reunião existente | `Informe uma reunião existente.` |
| `assistido_id` | opcional, assistido existente | `Assistido inexistente.` |
| `categoria` | opcional, até 80 caracteres, sem catálogo (decisão A2) | `A categoria aceita até 80 caracteres.` |

Campo fora da tabela → 422. Estado inicial: `aberta`, com o primeiro item de histórico gravado com o autor do token. Resposta 201 no formato do GET `/api/demandas/<id>`. A resposta não devolve dado de assistido além do id.

Cada demanda sai com: `id`, `descricao`, `categoria`, `prioridade`, `prazo`, `estado`, `vencida`, `responsavel_id`, `responsavel_nome`, `reuniao_id`, `assistido_id`, `criado_em`, `atualizado_em`, `ultimo_movimento` (momento do item de histórico mais recente).

`vencida` é verdadeiro quando o prazo é anterior a hoje, no fuso do CRIE, **e** a demanda não está concluída nem cancelada: demanda encerrada não está vencida. O cliente pinta o destaque; o servidor só calcula o booleano.

### GET `/api/demandas`

Filtros opcionais, combináveis:

| Filtro | Efeito |
| --- | --- |
| `estado` | um estado ou vários separados por vírgula (`aberta,em_andamento`); valor fora da lista → 422 |
| `responsavel_id` | do responsável atual |
| `categoria` | igual ao texto, sem diferenciar maiúscula |
| `periodo_inicio`, `periodo_fim` | data de registro da demanda, inclusivas (decisão A6) |
| `assistido_id` | ligadas ao assistido |
| `reuniao_id` | nascidas na reunião |
| `q` ou `busca` | trecho da descrição, sem diferenciar maiúscula (o card pediu `busca`; a spec dizia `q`; os dois valem) |

Sem filtro nenhum, lista as demandas não canceladas. Com qualquer filtro, só os filtros valem (inclusive para achar cancelada pela busca). Ordem: último movimento mais recente primeiro.

### GET `/api/demandas/<id>`

Demanda mais `historico` em ordem cronológica. Inexistente → 404, `{"erro": "Demanda inexistente."}`.

### GET `/api/demandas/<id>/historico`

Só o histórico, em ordem cronológica. Cada item: `id`, `tipo` (`estado` ou `anotacao`), `texto`, `estado_anterior`, `estado_novo`, `autor_id`, `autor_nome`, `ocorrido_em`.

### GET `/api/demandas/painel`

Painel das demandas em aberto (RF30, RF33, RF39). Só entram as não encerradas (`aberta`, `em_andamento`, `aguardando_terceiros`).

```json
{
  "por_estado": {"aberta": [...], "em_andamento": [...], "aguardando_terceiros": [...]},
  "totais": {"aberta": 2, "em_andamento": 3, "aguardando_terceiros": 1},
  "total": 6,
  "vencidas": 2
}
```

Em cada coluna, do prazo mais antigo para o mais novo: as vencidas ficam no topo. Coluna vazia vem `[]`.

### GET `/api/demandas/minhas`

As demandas em que o usuário do token é o responsável (RF34), não encerradas, do prazo mais antigo para o mais novo, cada uma com `vencida`. Com `estado`, vale o filtro (por exemplo `estado=concluida` para ver as que já fechou).

### PATCH `/api/demandas/<id>/estado`

Corpo: `{"estado": "..."}`.

Transições aceitas:

| De | Para |
| --- | --- |
| `aberta` | `em_andamento`, `cancelada` |
| `em_andamento` | `aguardando_terceiros`, `concluida`, `cancelada` |
| `aguardando_terceiros` | `em_andamento`, `cancelada` |

Qualquer outro par, inclusive sair de `concluida` ou de `cancelada`, → 400, `{"erro": "Esta demanda não pode mudar para esse estado."}`.

Ao aceitar, grava um item de histórico com o autor do token, a data e a hora. O item não tem rota de alteração nem de exclusão. Corpo sem `estado` → 422, `{"erro": "Informe o novo estado."}`. Resposta 200 no formato do GET `/api/demandas/<id>`.

### POST `/api/demandas/<id>/anotacoes`

Corpo: `{"texto": "..."}`. Texto vazio → 422, `{"erro": "Escreva o texto da anotação."}`. Vira item de histórico `anotacao`. Não muda o estado. Resposta 201: o item de histórico.

### PATCH `/api/demandas/<id>/responsavel`

Corpo: `{"responsavel_id": ...}`. Usuário inexistente ou inativo → 404, `{"erro": "Responsável inexistente ou inativo."}`. Grava anotação de sistema no histórico com o autor da troca. Resposta 200 no formato do GET `/api/demandas/<id>`.

Não há `DELETE`. Cancelar é mudança de estado.

---

## 2. Decisões abertas

| # | Decisão | Enquanto não fecha |
| --- | --- | --- |
| A6 | A que data o "período" do filtro (RF31) e do relatório (RF35) se refere: registro da demanda, data da reunião de origem ou prazo | data de registro da demanda (`criado_em`), no fuso do CRIE |

---

## 3. Testes que provam esta spec

- Criar demanda nasce `aberta` e gera histórico.
- `concluida` → `aberta` devolve 400 e não grava histórico novo.
- Anotação vazia devolve 422.
- Lista com prazo no passado marca `vencida: true`; demanda concluída com prazo no passado não.
- Pedido sem token devolve 401.
- A busca acha pelo trecho da descrição, em `q` e em `busca`.
- O painel separa por estado, deixa de fora as encerradas e conta as vencidas.
- `minhas` só traz as do usuário do token.

---

## 4. O que não entra

Encaminhamento, serviço da rede, retorno de acompanhamento, anexo de arquivo, exclusão definitiva e catálogo fechado de categorias.
