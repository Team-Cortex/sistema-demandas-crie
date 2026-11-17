# Spec 04 — Reunião

**Status:** fechada. Setores conforme o relato da direção no relatório v2.

Se esta spec divergir do código, a spec vence.

---

## 1. O que o servidor faz

Todas as rotas exigem token válido.

### POST `/api/reunioes`

Corpo: `data`, `setor`, `participante_ids`.

1. `data` ausente ou fora de `AAAA-MM-DD` → 422, `{"erro": "Informe a data da reunião."}`.
2. `setor` fora de `pedagogico`, `saude`, `convivencia` → 422, `{"erro": "Informe o setor da reunião."}`.
3. `participante_ids` vazio ou com usuário inexistente ou inativo → 422, `{"erro": "Informe participantes ativos."}`. Id repetido conta uma vez.
4. Campo fora dos três → 422.
5. Grava a reunião e a relação de presença. Não cria demanda automaticamente. Resposta 201 no formato do GET `/api/reunioes/<id>`.

### GET `/api/reunioes`

Lista por `data` decrescente; na mesma data, a registrada por último vem antes. Filtro opcional `setor`. Cada item: `id`, `data`, `setor`, `participantes` (`id`, `nome`).

### GET `/api/reunioes/<id>`

A reunião mais `demandas`: `id`, `descricao`, `estado` de cada demanda originada nela, na ordem de registro. Sem demanda, `demandas: []`. Inexistente → 404, `{"erro": "Reunião inexistente."}`.

### PATCH `/api/reunioes/<id>` (PUT aceito, mesmo efeito)

Pode alterar `data`, `setor` e `participante_ids`, um ou mais, com as mesmas regras do POST. Corpo sem nenhum dos três → 422. Não apaga demanda já ligada à reunião. O card pediu `PUT`; a rota aceita os dois verbos com o comportamento de PATCH.

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
