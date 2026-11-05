# Spec 02 — Demanda e estados

**Status:** fechada para a máquina de estados. A persistência espera o modelo relacional.  
Decisão de transição registrada pela frente de back-end em 13/10/2026. Se a instituição descrever outro fluxo, esta tabela é substituída, com data.

Se esta spec divergir do código, a spec vence.

---

## 1. O que o servidor faz

Todas as rotas exigem token válido.

### POST `/api/demandas`

Corpo:

| Campo | Regra |
| --- | --- |
| `descricao` | obrigatória, texto não vazio |
| `prioridade` | obrigatória: `baixa`, `media` ou `alta` |
| `responsavel_id` | obrigatório, usuário ativo |
| `prazo` | obrigatório, data |
| `reuniao_id` | obrigatória, reunião existente |
| `assistido_id` | opcional |
| `categoria` | opcional, até 80 caracteres, sem catálogo (decisão A2) |

Estado inicial: `aberta`. A resposta traz a demanda e não devolve dado clínico de assistido além do id.

### GET `/api/demandas`

Filtros opcionais: `estado`, `responsavel_id`, `periodo_inicio`, `periodo_fim`, `assistido_id`, `categoria`, `q` (busca na descrição). Sem filtro, lista as demandas não canceladas por último movimento. Prazo anterior a hoje vem com `"vencida": true`. O cliente pinta o destaque; o servidor só calcula o booleano.

### GET `/api/demandas/<id>`

Demanda mais `historico` em ordem cronológica. Cada item do histórico tem `autor_id`, `ocorrido_em`, `tipo` (`estado` ou `anotacao`) e `texto`.

### PATCH `/api/demandas/<id>/estado`

Corpo: `{"estado": "..."}`.

Transições aceitas:

| De | Para |
| --- | --- |
| `aberta` | `em_andamento`, `cancelada` |
| `em_andamento` | `aguardando_terceiros`, `concluida`, `cancelada` |
| `aguardando_terceiros` | `em_andamento`, `cancelada` |

Qualquer outro par, inclusive sair de `concluida` ou de `cancelada`, → 400, `{"erro": "Esta demanda não pode mudar para esse estado."}`.

Ao aceitar, grava um item de histórico com o autor do token, a data e a hora. O item não tem rota de alteração nem de exclusão.

### POST `/api/demandas/<id>/anotacoes`

Corpo: `{"texto": "..."}`. Texto vazio → 422. Vira item de histórico `anotacao`. Não muda o estado.

### PATCH `/api/demandas/<id>/responsavel`

Corpo: `{"responsavel_id": ...}`. Usuário inexistente ou inativo → 404. Grava anotação de sistema no histórico com o autor da troca.

Não há `DELETE`. Cancelar é mudança de estado.

---

## 2. Testes que provam esta spec

- Criar demanda nasce `aberta` e gera histórico.
- `concluida` → `aberta` devolve 400 e não grava histórico novo.
- Anotação vazia devolve 422.
- Lista com prazo no passado marca `vencida: true`.
- Pedido sem token devolve 401.

---

## 3. O que não entra

Encaminhamento, serviço da rede, retorno de acompanhamento, anexo de arquivo, exclusão definitiva e catálogo fechado de categorias.
