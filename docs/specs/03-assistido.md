# Spec 03 — Assistido

**Status:** fechada no contorno da rota. Os atributos de identificação esperam a decisão A3.  
Dado sensível: identificação e evolução de pessoa atendida, parte delas menor de idade. No repositório e na semente, só valor fictício.

Se esta spec divergir do código, a spec vence.

---

## 1. O que o servidor faz

Todas as rotas exigem token válido. Qualquer profissional ativo ou a direção acessa, conforme o relatório v2. Cada leitura e cada escrita gravam auditoria com `autor_id`, `acao`, `assistido_id` e `ocorrido_em` (tabela e regras na [spec 05](05-auditoria.md)). A auditoria não tem rota de apagar.

### POST `/api/assistidos`

Enquanto A3 estiver aberta, o único campo aceito é `nome_tratamento` (texto não vazio, fictício, até 120 caracteres). Qualquer outro campo no corpo → 422, `{"erro": "Este dado ainda não foi autorizado pela instituição."}`. Sem `nome_tratamento` → 422, `{"erro": "Informe o nome de tratamento."}`. Resposta 201 no formato do GET `/api/assistidos/<id>`.

Não se pede documento, data de nascimento, diagnóstico, nome de familiar nem contato.

### GET `/api/assistidos` e GET `/api/assistidos/<id>`

A lista devolve `id` e `nome_tratamento`, em ordem alfabética, com filtro opcional `busca` (trecho do nome). A auditoria da lista guarda que houve busca, nunca o texto buscado. O registro devolve também `ativo`, `criado_em` e três listas de ids, em ordem cronológica: `demandas`, `evolucoes` (só a versão vigente de cada uma), `encaminhamentos`. Lista vazia vem `[]`, nunca campo omitido. Inexistente → 404, `{"erro": "Assistido inexistente."}`.

### GET `/api/assistidos/<id>/ficha`

A ficha completa (RF20), em ordem cronológica: `assistido` (`id`, `nome_tratamento`, `ativo`), `profissionais` que acompanham (`id`, `nome`), `demandas` (no formato da spec 02), `evolucoes` vigentes (no formato da spec 06) e `encaminhamentos` (no formato da spec 07). Lista vazia vem `[]`.

Como traz evolução, a ficha passa por `pode_ver_evolucao(assistido)`: quem não pode → 403, `{"erro": "Você não tem acesso às evoluções deste assistido."}`, sem registro de auditoria. Com o acesso aberto de hoje, todo profissional ativo e a direção passam.

### PATCH `/api/assistidos/<id>` (PUT aceito, mesmo efeito)

Mesma regra do POST: só `nome_tratamento`. Não há `DELETE`. O card pediu `PUT`; a rota aceita os dois verbos com o mesmo efeito, já que há um campo só.

---

## 2. Evolução, encaminhamento e relatório

A ficha aponta para esses registros. Criar evolução, encaminhar à rede e emitir relatório não entram nesta spec: estão nas specs [06](06-evolucao.md), [07](07-encaminhamento.md) e [08](08-relatorio.md). Evolução continua sendo dado de acompanhamento da pessoa, distinto do histórico da demanda.

---

## 3. Testes que provam esta spec

- POST com `data_nascimento` devolve 422 e não grava.
- POST só com `nome_tratamento` grava e gera auditoria de criação.
- GET da ficha gera auditoria de consulta.
- Sem token, 401, e não grava auditoria de leitura do assistido.
- Com a regra restritiva ligada, quem não acompanha o assistido recebe 403 na ficha.

---

## 4. O que não entra

Documento de identificação, dado de saúde, familiar, foto, evolução lançada por esta rota, encaminhamento e exportação.
