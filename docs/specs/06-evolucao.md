# Spec 06 — Evolução do assistido

**Status:** fechada para implementação no servidor. O model já existe (card #54); esta spec fecha a rota.
**Origem:** RF21 a RF26, RNF01, RNF03, proposta do `contrato-api.md` de 13/10/2026.
Dado sensível: acompanhamento de pessoa atendida, parte delas menor de idade. No repositório e na semente, só texto fictício.

Se esta spec divergir do código, a spec vence.

---

## 1. O que o servidor faz

Todas as rotas exigem token válido e passam por `pode_ver_evolucao(assistido)`. Quem não pode → 403, `{"erro": "Você não tem acesso às evoluções deste assistido."}`. Com o acesso aberto de hoje (spec 01 §2), todo profissional ativo e a direção passam. Cada operação grava auditoria (spec 05).

Cada evolução sai com: `id`, `assistido_id`, `data`, `area_atuacao`, `descricao`, `profissional_id`, `profissional_nome`, `autor_id`, `autor_nome`, `ocorrido_em`, `retifica_id` (a versão que ela corrige, ou vazio) e `vigente`.

### POST `/api/assistidos/<assistido_id>/evolucoes`

Corpo: `data` (`AAAA-MM-DD`), `area_atuacao` (texto até 80, sem catálogo enquanto QA06 não fecha) e `descricao`.

1. Assistido inexistente → 404, `{"erro": "Assistido inexistente."}`.
2. Sem permissão → 403.
3. Campo faltando ou vazio → 422: `Informe a data da evolução.`, `Informe a área de atuação.`, `Escreva a descrição da evolução.` Área com mais de 80 caracteres → 422. Campo fora dos três → 422.
4. Autor e profissional responsável saem do token; `ocorrido_em` é do servidor (RF22). O corpo não escolhe nenhum dos três.
5. Resposta 201: a evolução.

### GET `/api/assistidos/<assistido_id>/evolucoes`

Só as versões vigentes, em ordem cronológica pela `data` (RF23). Filtros opcionais (RF25): `de` e `ate` (inclusivas, sobre a `data`) e `area_atuacao` (igual, sem diferenciar maiúscula). A auditoria guarda os filtros usados.

### GET `/api/evolucoes/<id>`

A evolução mais `versoes_anteriores` (da mais recente para a original) e `retificada_por_id` (a versão que a substituiu, ou vazio). Serve para ver o que foi corrigido (RF24). Inexistente → 404, `{"erro": "Evolução inexistente."}`.

### PATCH `/api/evolucoes/<id>`

Retifica (RF24). Corpo com um ou mais de `data`, `area_atuacao`, `descricao`; corpo vazio → 422, `{"erro": "Informe o que muda na retificação."}`.

1. Cria uma versão nova, com autor do token e momento do servidor, apontando a anterior em `retifica_id`. A anterior fica como estava.
2. Só a versão vigente se retifica; retificar uma antiga → 400, `{"erro": "Só a versão vigente da evolução pode ser retificada."}`.
3. Resposta 201: a versão nova (id novo). É 201 porque nasce um registro; nada é sobrescrito.

### Sem exclusão

Não existe `DELETE` (RF26): a rota responde 405. A sessão do ORM e o trigger do banco também recusam (migração `b0f13416410c`).

## 2. Decisões abertas

| # | Decisão | Enquanto não fecha |
| --- | --- | --- |
| A9 | Quem pode retificar: só o autor, o autor e a direção, ou quem pode ver | quem pode ver pode retificar; autor e momento da retificação ficam gravados e auditados |
| QA06 | Lista de áreas de atuação | texto livre de até 80 caracteres |

## 3. Testes que provam esta spec

- Lançar grava autor, profissional e momento do servidor, e gera auditoria `criar`.
- A lista vem em ordem cronológica e filtra por período e área.
- Retificar cria versão nova, a anterior continua igual e sai da lista; retificar a antiga dá 400.
- `DELETE` dá 405 e nada sai do banco.
- Com a regra restritiva ligada, quem não acompanha recebe 403 em todas as rotas, e nada é gravado.

## 4. O que não entra

Anexo, assinatura digital, exclusão, edição sem nova versão e catálogo fechado de áreas.
