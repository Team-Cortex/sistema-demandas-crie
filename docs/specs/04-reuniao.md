# Spec 04 — Reunião

**Status:** fechada. Setores conforme o relato da direção no relatório v2.

Se esta spec divergir do código, a spec vence.

---

## 1. O que o servidor faz

Todas as rotas exigem token válido.

### POST `/api/reunioes`

Corpo: `data`, `setor`, `participante_ids`.

1. `setor` fora de `pedagogico`, `saude`, `convivencia` → 422, `{"erro": "Informe o setor da reunião."}`.
2. `participante_ids` vazio ou com usuário inexistente ou inativo → 422, `{"erro": "Informe participantes ativos."}`.
3. Grava a reunião e a relação de presença. Não cria demanda automaticamente.

### GET `/api/reunioes`

Lista por `data` decrescente. Cada item: `id`, `data`, `setor`, `participantes` (`id`, `nome`).

### GET `/api/reunioes/<id>`

A reunião mais `demandas`: `id`, `descricao`, `estado` de cada demanda originada nela. Sem demanda, `demandas: []`.

### PATCH `/api/reunioes/<id>`

Pode alterar `data`, `setor` e `participante_ids`, com as mesmas regras do POST. Não apaga demanda já ligada à reunião.

Não há `DELETE`.

---

## 2. Testes que provam esta spec

- Setor desconhecido devolve 422.
- Lista vem da data mais recente para a mais antiga.
- A ficha da reunião mostra o estado atual das demandas originadas nela.
- Sem token, 401.

---

## 3. O que não entra

Ata em texto livre, anexo, recorrência automática das três reuniões semanais e criação de demanda dentro do POST da reunião. A demanda nasce na spec 02, apontando `reuniao_id`.
