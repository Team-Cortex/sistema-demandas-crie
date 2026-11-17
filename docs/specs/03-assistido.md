# Spec 03 — Assistido

**Status:** fechada no contorno da rota. Os atributos de identificação esperam a decisão A3.  
Dado sensível: identificação e evolução de pessoa atendida, parte delas menor de idade. No repositório e na semente, só valor fictício.

Se esta spec divergir do código, a spec vence.

---

## 1. O que o servidor faz

Todas as rotas exigem token válido. Qualquer profissional ativo ou a direção acessa, conforme o relatório v2. Cada leitura e cada escrita gravam auditoria com `autor_id`, `acao`, `assistido_id` e `ocorrido_em`. A auditoria não tem rota de apagar.

### POST `/api/assistidos`

Enquanto A3 estiver aberta, o único campo aceito é `nome_tratamento` (texto não vazio, fictício). Qualquer outro campo no corpo → 422, `{"erro": "Este dado ainda não foi autorizado pela instituição."}`.

Não se pede documento, data de nascimento, diagnóstico, nome de familiar nem contato.

### GET `/api/assistidos` e GET `/api/assistidos/<id>`

A lista devolve `id` e `nome_tratamento`. A ficha devolve também três listas de ids, em ordem cronológica: `demandas`, `evolucoes`, `encaminhamentos`. Lista vazia vem `[]`, nunca campo omitido.

### PATCH `/api/assistidos/<id>`

Mesma regra do POST: só `nome_tratamento`. Não há `DELETE`.

---

## 2. Evolução, encaminhamento e relatório

A ficha aponta para esses registros. Criar evolução, encaminhar à rede e emitir relatório não entram nesta spec. Evolução continua sendo dado de acompanhamento da pessoa, distinto do histórico da demanda.

---

## 3. Testes que provam esta spec

- POST com `data_nascimento` devolve 422 e não grava.
- POST só com `nome_tratamento` grava e gera auditoria de criação.
- GET da ficha gera auditoria de consulta.
- Sem token, 401, e não grava auditoria de leitura do assistido.

---

## 4. O que não entra

Documento de identificação, dado de saúde, familiar, foto, evolução lançada por esta rota, encaminhamento e exportação.
